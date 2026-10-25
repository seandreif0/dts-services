# it-asset-inventory

Sample Flask service for IT asset inventory.

## Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `DB_HOST` | Empty | Database host. |
| `DB_PORT` | `1433` | Database port. |
| `DB_NAME` | `ITAM` | Database name. |
| `DB_USER` | Empty | Database user. |
| `DB_PASSWORD_SECRET_NAME` | `dts/it-asset-inventory/db` | AWS Secrets Manager secret name whose `SecretString` is the database password, resolved at runtime on first database use. The service needs AWS credentials and a region from the environment, such as an attached task role and `AWS_REGION`. |
| `LOG_LEVEL` | `INFO` | Application log level. |
| `PORT` | `8080` | HTTP server port. |

Application logs are written to stdout. `GET /healthz` returns `{"status":"ok"}` without accessing the database.

## Local development

```sh
pip install -r requirements.txt
python app.py
pytest
```

## Docker

```sh
docker build -t dts-it-asset-inventory .
docker run -p 8080:8080 \
  -e DB_HOST='<db-host>' \
  -e DB_USER='<db-user>' \
  -e DB_PASSWORD_SECRET_NAME=dts/it-asset-inventory/db \
  dts-it-asset-inventory
curl localhost:8080/healthz
```
