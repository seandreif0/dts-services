# badge-access

An internal DTS service packaged as a container.

## Configuration

| Environment variable | Default | Description |
| --- | --- | --- |
| `DB_HOST` | Empty | Database host |
| `DB_PORT` | `1433` | Database port |
| `DB_NAME` | `BADGE` | Database name |
| `DB_USER` | Empty | Database user |
| `DB_PASSWORD_SECRET_NAME` | `dts/badge-access/db` | AWS Secrets Manager secret name; its `SecretString` is the database password and is resolved at runtime only when a database connection string is built |
| `LOG_LEVEL` | `INFO` | Logging level |
| `PORT` | `8080` | HTTP port |

Logs go to stdout. `GET /healthz` returns `{"status": "ok"}`.

## Local development

```sh
python3.11 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m pytest -v
python app.py
```

## Docker

```sh
docker build -t dts-badge-access .
docker run --rm -p 8080:8080 -e DB_HOST=... -e DB_USER=... -e DB_PASSWORD_SECRET_NAME=dts/badge-access/db dts-badge-access
curl localhost:8080/healthz
```
