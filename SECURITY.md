# Security reporting and operating guidance

## Send vulnerability reports privately

Do not disclose a security issue in a public ticket. Submit a private
advisory through GitHub:

```text
https://github.com/gaurzamdev/SageCircuit/security/advisories/new
```

Please provide:

- the affected version or commit,
- a minimal reproduction,
- the impact you believe is possible,
- any suggested fix or mitigation.

Maintainers will acknowledge the report as soon as reasonably possible. Give
them time to investigate, prepare a fix, and coordinate disclosure before
sharing details publicly.

## Versions receiving fixes

Updates are made for the current release line. Previous model snapshots and
independent forks are outside the supported set.

## Protecting the local server

SageCircuit's web console and API use a local HTTP server intended for one trusted user
on `127.0.0.1`. It currently has these limitations:

- There is no authentication or authorization.
- CORS is permissive for local development.
- Request bodies are not rate-limited.
- The server is not hardened for exposure to the public internet.

Avoid binding to `0.0.0.0` on an untrusted network. If remote access is
necessary, place the server behind a reverse proxy that supplies TLS,
authentication, request limits, and logging.

## Treat model containers as untrusted input

Application code parses `.tsei` and `.pyz` files. Before using a file from an
untrusted source, inspect the parser and test the file in an isolated
environment. A crafted container could consume excessive memory or disrupt
service.

## Keep credentials out of the repository

No Android signing key is supplied here. Never commit `.jks`, `.keystore`,
`.p12`, `.pfx`, passwords, API tokens, or private keys. If any credential is
exposed, revoke or rotate it promptly.

## Build dependencies and automation

The build pipeline installs a pinned numpy release on GitHub-hosted runners.
Actions are configured with limited permissions and build jobs do not receive
repository secrets. CodeQL and Dependabot are enabled.

## Reports outside this policy

- Incorrect answers; refer to the model limitations instead.
- Prompt injection or output-quality concerns that do not cross a security
  boundary.
- Problems in third-party providers or websites accessed through optional web
  research.
- Service interruption caused by deliberately loading an untrusted model on a
  machine you control.
