# training-catalog

Internal DTS training catalog service.

## Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `DB_HOST` | empty | Database hostname |
| `DB_PORT` | `1433` | Database port |
| `DB_NAME` | `LMS` | Database name |
| `DB_USER` | empty | Database user |
| `DB_PASSWORD_SECRET_NAME` | `dts/training-catalog/db` | AWS Secrets Manager secret name. Its `SecretString` is the database password and is resolved at runtime. AWS credentials and `AWS_REGION` are needed only when the database is used. |
| `LOG_LEVEL` | `INFO` | Logging level |
| `PORT` | `8080` | HTTP listen port |

Application logs are written to stdout. `GET /healthz` returns `{"status":"ok"}` without accessing the database.

## Local development

```sh
pip install -r requirements.txt
python app.py
pytest
```

## Docker

```sh
docker build -t dts-training-catalog .
docker run -p 8080:8080 -e DB_HOST=... -e DB_USER=... dts-training-catalog
```
