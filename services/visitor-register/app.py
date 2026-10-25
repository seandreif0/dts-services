import logging

from flask import Flask, abort, jsonify

import config
from data import RECORDS


def setup_logging(app):
    handler = logging.FileHandler(app.config["LOG_FILE"])
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    app.logger.addHandler(handler)
    app.logger.setLevel(app.config["LOG_LEVEL"])


def db_dsn(cfg):
    return "mssql://{user}:{pw}@{host}:{port}/{name}".format(
        user=cfg["DB_USER"], pw=cfg["DB_PASSWORD"], host=cfg["DB_HOST"], port=cfg["DB_PORT"], name=cfg["DB_NAME"]
    )


def create_app(overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)
    if overrides:
        app.config.update(overrides)
    setup_logging(app)
    app.logger.info("connecting to %s", app.config["DB_HOST"])

    @app.get("/visitors")
    def list_items():
        return jsonify(RECORDS)

    @app.get("/visitors/<item_id>")
    def get_item(item_id):
        for r in RECORDS:
            if r["visit_id"] == item_id:
                return jsonify(r)
        abort(404)

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=config.PORT)
