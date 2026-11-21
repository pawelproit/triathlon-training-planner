from flask import Blueprint

bp = Blueprint("workouts", __name__)

from . import routes  # noqa: E402,F401