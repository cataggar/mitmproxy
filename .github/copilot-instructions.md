# Copilot instructions — cataggar/mitmproxy

## Repo topology

This is a personal mirror, not the upstream project.

- **Default branch is `mirror`** — a *tooling-only* branch holding
  `.github/workflows/` + `scripts/`. It is the default so that
  `workflow_dispatch` works: a workflow is only dispatchable via the API / `gh`
  if its file exists on the default branch.
- **`main`** — a mirror of the upstream mitmproxy source. Do not add mirror
  tooling here.

## Conventions

- Direct all changes/PRs to `cataggar/mitmproxy`. Do **not** open PRs, issues, or
  comments on the upstream `mitmproxy/mitmproxy` repo.
- Release binaries are mirrored unchanged from `downloads.mitmproxy.org`; never
  rebuild or modify them.
- Rely on mitmproxy's build-provenance attestation (`mitmproxy-<v>.sigstore`,
  verified with `gh attestation verify ... --repo mitmproxy/mitmproxy`) for
  tamper-evidence. Do not publish `.sha256` checksum sidecars.
- Tag releases as `v<version>` to match upstream tag names.
- Include this trailer on every commit:
  `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`
