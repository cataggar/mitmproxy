# cataggar/mitmproxy

A personal mirror of [mitmproxy](https://mitmproxy.org) that republishes the
official release binaries as GitHub Releases.

## Branches

- **`main`** — a mirror of the upstream mitmproxy source from
  [mitmproxy/mitmproxy](https://github.com/mitmproxy/mitmproxy).
- **`mirror`** (default) — release/CI tooling only: the workflows and scripts
  that mirror official mitmproxy release binaries into this repo's Releases.

## Why this exists

The mitmproxy project ships its release binaries to
<https://downloads.mitmproxy.org/> — the upstream GitHub Releases carry no
binary assets. This repo mirrors those binaries (unchanged) into GitHub Releases
so they can be installed and verified through GitHub tooling.

## Releases

Each release contains the official mitmproxy artifacts for a version, copied
byte-for-byte from `https://downloads.mitmproxy.org/<version>/`, including
mitmproxy's build-provenance attestation bundle `mitmproxy-<version>.sigstore`
(produced upstream by `actions/attest-build-provenance`).

Verify any asset against that bundle with the [`gh` CLI](https://cli.github.com/):

```sh
gh attestation verify mitmproxy-12.2.3-linux-x86_64.tar.gz \
  --bundle mitmproxy-12.2.3.sigstore --repo mitmproxy/mitmproxy
```

The attestation provides tamper-evidence, so no `.sha256` sidecar files are
published.

## Mirroring a release

`workflow_dispatch` the **Publish mitmproxy Release** workflow with a `version`
(e.g. `12.2.3`). It downloads every asset from `downloads.mitmproxy.org`,
verifies each one against the provenance bundle, and creates a `v<version>`
GitHub Release.

The **Check for new mitmproxy release** workflow (manual trigger) finds the
latest published version and, if it is not yet mirrored, tags it and dispatches
the publish workflow.
