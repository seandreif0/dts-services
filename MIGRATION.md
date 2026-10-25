# DTS services: cloud migration standard

All six services under `services/` are moving from on-prem VMs to containers on AWS. Each service is migrated in its own pull request and must meet every item below. Keep changes to the service's own folder.

## Current state (on-prem)

- `config.py` hardcodes the database host, user and **password**.
- Logs go to a file under `/var/log/dts/`.
- No health check endpoint.
- No Dockerfile; deployed by copying files onto a VM.

## Target state

1. **Configuration from environment variables.** `config.py` reads every setting from `os.environ` with a sensible non-secret default where one makes sense (e.g. `PORT=8080`, `LOG_LEVEL=INFO`). `DB_HOST`, `DB_PORT`, `DB_NAME` and `DB_USER` come from env vars with no on-prem hostname left in code.
2. **Secrets by reference, never by value.** Remove the hardcoded password. The service reads `DB_PASSWORD_SECRET_NAME` (an AWS Secrets Manager secret name, for example `dts/<service>/db`) and resolves it at runtime. No secret value may appear in code, tests, the Dockerfile, docs or commit history. Tests must not call AWS; stub the lookup.
3. **Logging to stdout.** Replace the file handler with a `StreamHandler` to stdout. No paths under `/var/log`.
4. **Health check.** Add `GET /healthz` returning HTTP 200 and `{"status": "ok"}` without touching the database.
5. **Dockerfile.** Add `services/<service>/Dockerfile` based on `python:3.11-slim`, runs as a non-root user, installs `requirements.txt`, exposes `8080`, and starts the app. Add a `.dockerignore`.
6. **Tests still pass.** All existing tests pass. Add tests for `/healthz` and for config coming from environment variables.

## Definition of done (per service PR)

- [ ] No hostnames, users or passwords hardcoded in `config.py`
- [ ] `DB_PASSWORD_SECRET_NAME` used; no secret values anywhere
- [ ] Logs to stdout only
- [ ] `/healthz` returns 200
- [ ] `Dockerfile` and `.dockerignore` present; `docker build` succeeds
- [ ] `pytest` passes in the service folder
- [ ] PR title: `DTS-MIG: <service> to container-ready config`
