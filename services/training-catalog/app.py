import logging
import sys

import boto3
from flask import Flask, abort, jsonify

import config
from data import RECORDS


def setup_logging(app):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    app.logger.addHandler(handler)
    app.logger.setLevel(app.config["LOG_LEVEL"])


def get_db_password(secret_name):
    client = boto3.client("secretsmanager")
    return client.get_secret_value(SecretId=secret_name)["SecretString"]


def db_dsn(cfg):
    pw = get_db_password(cfg["DB_PASSWORD_SECRET_NAME"])
    return "mssql://{user}:{pw}@{host}:{port}/{name}".format(
        user=cfg["DB_USER"], pw=pw, host=cfg["DB_HOST"], port=cfg["DB_PORT"], name=cfg["DB_NAME"]
    )


def create_app(overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)
    if overrides:
        app.config.update(overrides)
    setup_logging(app)
    app.logger.info("connecting to %s", app.config["DB_HOST"])

    @app.get("/healthz")
    def healthz():
        return jsonify(status="ok")

    @app.get("/courses")
    def list_items():
        return jsonify(RECORDS)

    @app.get("/courses/<item_id>")
    def get_item(item_id):
        for r in RECORDS:
            if r["course_id"] == item_id:
                return jsonify(r)
        abort(404)

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=config.PORT)
