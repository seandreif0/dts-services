# visitor-register

Internal DTS service. Container-ready: configured from environment variables, logs to stdout.

## Configuration

| Variable | Default | Notes |
| --- | --- | --- |
| `DB_HOST` | _(none)_ | Database host |
| `DB_PORT` | `1433` | Database port |
| `DB_NAME` | _(none)_ | Database name |
| `DB_USER` | _(none)_ | Database user |
| `DB_PASSWORD_SECRET_NAME` | `dts/visitor-register/db` | AWS Secrets Manager secret **name**; the password is resolved at runtime, only when a DB connection string is built |
| `LOG_LEVEL` | `INFO` | |
| `PORT` | `8080` | |

`GET /healthz` returns `{"status": "ok"}` without touching the database.

## Run locally

```sh
pip install -r requirements.txt
python app.py
pytest
```

## Docker

```sh
docker build -t dts-visitor-register .
docker run --rm -p 8080:8080 \
  -e DB_HOST=<host> -e DB_NAME=<name> -e DB_USER=<user> \
  -e DB_PASSWORD_SECRET_NAME=dts/visitor-register/db \
  dts-visitor-register
curl localhost:8080/healthz
```

AWS credentials/region for Secrets Manager come from the standard AWS environment (e.g. task role).
