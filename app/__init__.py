from flask import Flask

from config import Config

from .extensions import csrf, db, login_manager, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from . import models  # noqa: F401  (żeby migracje widziały modele)
    from .main import bp as main_bp

    app.register_blueprint(main_bp)

    return app