#!/usr/bin/env python3
"""Check for a new mitmproxy release and signal when to mirror it.

Discovers the latest version directory published to downloads.mitmproxy.org
(the same source the website uses) and, if our mirror repository does not yet
have a matching ``v<version>`` tag, writes ``new_version`` to ``$GITHUB_OUTPUT``.
"""

# /// script
# requires-python = ">=3.12"
# dependencies = ["requests"]
# ///

import logging
import os
import re
import xml.etree.ElementTree as ET

import requests  # type: ignore[import-untyped]

BUCKET_LIST = "https://downloads.mitmproxy.org/list"
S3_NS = "{http://s3.amazonaws.com/doc/2006-03-01/}"
VERSION_RE = re.compile(r"^[\d.]+$")

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def github_headers() -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def list_versions() -> list[str]:
    """Return published version directories, newest first."""
    resp = requests.get(BUCKET_LIST, params={"delimiter": "/", "prefix": ""}, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    versions = []
    for cp in root.findall(f"{S3_NS}CommonPrefixes"):
        prefix_el = cp.find(f"{S3_NS}Prefix")
        if prefix_el is None or not prefix_el.text:
            continue
        name = prefix_el.text.rstrip("/")
        if VERSION_RE.match(name):
            versions.append(name)
    versions.sort(key=lambda v: [int(p) for p in v.split(".")], reverse=True)
    return versions


def tag_exists(repo: str, tag: str) -> bool:
    url = f"https://api.github.com/repos/{repo}/git/ref/tags/{tag}"
    resp = requests.get(url, headers=github_headers(), timeout=30)
    if resp.status_code == 200:
        return True
    if resp.status_code == 404:
        return False
    resp.raise_for_status()
    return False


def set_github_output(name: str, value: str) -> None:
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"{name}={value}\n")
    else:
        log.info("GITHUB_OUTPUT not set (running locally?); would set %s=%s", name, value)


def main() -> None:
    repo = os.environ.get("GITHUB_REPOSITORY", "cataggar/mitmproxy")
    log.info("Checking for new mitmproxy releases...")

    versions = list_versions()
    if not versions:
        log.error("No version directories found at downloads.mitmproxy.org")
        set_github_output("new_version", "")
        return

    latest = versions[0]
    tag = f"v{latest}"
    log.info("Latest published version: %s", latest)

    if tag_exists(repo, tag):
        log.info("Tag %s already exists in %s -- nothing to do", tag, repo)
        set_github_output("new_version", "")
        return

    log.info("New release to mirror: %s", latest)
    set_github_output("new_version", latest)


if __name__ == "__main__":
    main()
