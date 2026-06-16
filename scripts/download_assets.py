#!/usr/bin/env python3
"""Download official mitmproxy release assets from downloads.mitmproxy.org.

The mitmproxy project publishes its release binaries to an S3/R2 bucket served
at https://downloads.mitmproxy.org/<version>/ (the GitHub release itself carries
no binary assets). Every release also ships a single build-provenance
attestation bundle, ``mitmproxy-<version>.sigstore``, produced by
``actions/attest-build-provenance`` over all artifacts.

This script lists the bucket directory for a version, downloads every asset into
``dist/`` and -- when the ``gh`` CLI is available -- verifies each artifact
against the mirrored ``.sigstore`` bundle with ``gh attestation verify``.
"""

# /// script
# requires-python = ">=3.12"
# dependencies = ["requests"]
# ///

import logging
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import requests  # type: ignore[import-untyped]

WEB_ROOT = "https://downloads.mitmproxy.org/"
BUCKET_LIST = "https://downloads.mitmproxy.org/list"
S3_NS = "{http://s3.amazonaws.com/doc/2006-03-01/}"
# mitmproxy signs releases via actions/attest-build-provenance in this repo.
UPSTREAM_REPO = "mitmproxy/mitmproxy"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def list_assets(version: str) -> list[str]:
    """Return the asset keys (filenames) published for ``version``."""
    resp = requests.get(
        BUCKET_LIST, params={"delimiter": "/", "prefix": f"{version}/"}, timeout=30
    )
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    prefix = f"{version}/"
    keys = []
    for contents in root.findall(f"{S3_NS}Contents"):
        key_el = contents.find(f"{S3_NS}Key")
        if key_el is None or not key_el.text:
            continue
        name = key_el.text[len(prefix):] if key_el.text.startswith(prefix) else key_el.text
        if name:
            keys.append(name)
    return sorted(keys)


def download_file(url: str, dest: Path) -> None:
    """Download ``url`` to ``dest`` with simple progress logging."""
    log.info("  Downloading %s ...", dest.name)
    resp = requests.get(url, stream=True, timeout=600)
    resp.raise_for_status()
    total = int(resp.headers.get("content-length", 0))
    downloaded = 0
    next_log = 10
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8 * 1024 * 1024):
            f.write(chunk)
            downloaded += len(chunk)
            if total > 0:
                pct = downloaded * 100 // total
                if pct >= next_log:
                    log.info("    %d MB (%d%%)", downloaded // (1024 * 1024), pct)
                    next_log = pct - (pct % 10) + 10
    log.info("  Saved %s (%d MB)", dest.name, dest.stat().st_size // (1024 * 1024))


def verify_attestation(artifact: Path, bundle: Path) -> bool:
    """Verify ``artifact`` against the provenance ``bundle`` via the gh CLI.

    ``gh attestation verify`` requires the bundle to have a ``.json``/``.jsonl``
    extension, but mitmproxy publishes it as ``mitmproxy-<v>.sigstore``; pass a
    ``.json`` copy so we can verify the asset as mirrored.
    """
    try:
        subprocess.run(
            [
                "gh",
                "attestation",
                "verify",
                str(artifact),
                "--bundle",
                str(bundle),
                "--repo",
                UPSTREAM_REPO,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        log.error("  ATTESTATION FAILED for %s:\n%s", artifact.name, e.stderr.strip())
        return False
    log.info("  attestation OK: %s", artifact.name)
    return True


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <version>")
        print(f"Example: {sys.argv[0]} 12.2.3")
        sys.exit(1)

    version = sys.argv[1].lstrip("v")
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)

    log.info("Listing assets for mitmproxy %s ...", version)
    assets = list_assets(version)
    if not assets:
        log.error("No assets found for version %s at %s", version, WEB_ROOT)
        sys.exit(1)
    log.info("Found %d assets\n", len(assets))

    for name in assets:
        log.info("[%s]", name)
        download_file(f"{WEB_ROOT}{version}/{name}", dist_dir / name)
        log.info("")

    bundle = dist_dir / f"mitmproxy-{version}.sigstore"
    if not bundle.exists():
        log.error("Provenance bundle %s not found -- refusing to publish", bundle.name)
        sys.exit(1)

    if shutil.which("gh") is None:
        log.warning("gh CLI not found; skipping provenance verification")
    else:
        log.info("Verifying build provenance against %s ...", bundle.name)
        # gh requires a .json/.jsonl bundle extension; the published asset is
        # named *.sigstore, so verify against a temporary .json copy.
        with tempfile.TemporaryDirectory() as tmp:
            json_bundle = Path(tmp) / "bundle.sigstore.json"
            shutil.copyfile(bundle, json_bundle)
            failed = [
                f.name
                for f in sorted(dist_dir.iterdir())
                if f != bundle and not verify_attestation(f, json_bundle)
            ]
        if failed:
            log.error("%d artifacts failed provenance verification: %s", len(failed), failed)
            sys.exit(1)

    files = sorted(dist_dir.iterdir())
    total = sum(f.stat().st_size for f in files)
    log.info("Done! %d files in %s/ (%.1f MB total)", len(files), dist_dir, total / (1024**2))
    for f in files:
        log.info("  %s (%.1f MB)", f.name, f.stat().st_size / (1024**2))


if __name__ == "__main__":
    main()
