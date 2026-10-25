# desk-booking

Internal DTS service. Runs as a container; all configuration comes from environment variables.

| Variable | Default | Notes |
| --- | --- | --- |
| `DB_HOST` | _(none)_ | Database host |
| `DB_PORT` | `1433` | Database port |
| `DB_NAME` | _(none)_ | Database name |
| `DB_USER` | _(none)_ | Database user |
| `DB_PASSWORD_SECRET_NAME` | `dts/desk-booking/db` | AWS Secrets Manager secret **name**; the password is resolved at runtime when a DB connection is needed. The secret may be a plain string or JSON with a `password` key. |
| `LOG_LEVEL` | `INFO` | Logs go to stdout |
| `PORT` | `8080` | HTTP port |

AWS credentials and region are taken from the standard AWS environment (e.g. the task/instance role and `AWS_REGION`).

Health check: `GET /healthz` returns `{"status": "ok"}` without touching the database.

## Local

```sh
pip install -r requirements.txt
python app.py
pytest
```

## Docker

```sh
docker build -t dts-desk-booking .
docker run --rm -p 8080:8080 \
  -e DB_HOST=<host> -e DB_NAME=<name> -e DB_USER=<user> \
  -e DB_PASSWORD_SECRET_NAME=dts/desk-booking/db \
  -e AWS_REGION=<region> \
  dts-desk-booking
curl localhost:8080/healthz
```
