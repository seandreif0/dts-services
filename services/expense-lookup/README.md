# expense-lookup

Internal DTS service. Runs as a container; all configuration comes from environment variables.

| Variable | Default | Description |
| --- | --- | --- |
| `DB_HOST` | _(none)_ | Database host |
| `DB_PORT` | `1433` | Database port |
| `DB_NAME` | _(none)_ | Database name |
| `DB_USER` | _(none)_ | Database user |
| `DB_PASSWORD_SECRET_NAME` | `dts/expense-lookup/db` | AWS Secrets Manager secret **name** holding the DB password; resolved at runtime, only when a DB connection is built |
| `AWS_REGION` | _(none)_ | AWS region for Secrets Manager |
| `LOG_LEVEL` | `INFO` | Log level; logs go to stdout |
| `PORT` | `8080` | HTTP port |

Health check: `GET /healthz` returns `{"status": "ok"}` without touching the database.

```sh
docker build -t dts-expense-lookup .
docker run --rm -p 8080:8080 \
  -e DB_HOST=... -e DB_NAME=... -e DB_USER=... \
  -e DB_PASSWORD_SECRET_NAME=dts/expense-lookup/db -e AWS_REGION=... \
  dts-expense-lookup
curl localhost:8080/healthz
```

Local development:

```sh
pip install -r requirements.txt
python app.py
pytest
```
