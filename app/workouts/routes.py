from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..models import DISCIPLINES, Workout
from . import bp
from .forms import WorkoutForm

PER_PAGE = 10


def _get_own_workout_or_404(workout_id):
    """Zwraca trening tylko wtedy, gdy należy do zalogowanego użytkownika."""
    workout = db.session.get(Workout, workout_id)
    if workout is None or workout.user_id != current_user.id:
        abort(404)
    return workout


def _fill_workout(workout, form):
    workout.discipline = form.discipline.data
    workout.workout_date = form.workout_date.data
    workout.duration_min = form.duration_min.data
    workout.distance_km = form.distance_km.data
    workout.rpe = form.rpe.data
    workout.notes = (form.notes.data or "").strip() or None


@bp.route("/")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    discipline = request.args.get("discipline")
    if discipline not in dict(DISCIPLINES):
        discipline = None

    query = db.select(Workout).where(Workout.user_id == current_user.id)
    if discipline:
        query = query.where(Workout.discipline == discipline)
    query = query.order_by(Workout.workout_date.desc(), Workout.id.desc())

    pagination = db.paginate(query, page=page, per_page=PER_PAGE, error_out=False)
    return render_template(
        "workouts/list.html",
        pagination=pagination,
        disciplines=DISCIPLINES,
        current_discipline=discipline,
    )


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = WorkoutForm()
    if form.validate_on_submit():
        workout = Workout(user_id=current_user.id)
        _fill_workout(workout, form)
        db.session.add(workout)
        db.session.commit()
        flash("Trening został dodany.", "success")
        return redirect(url_for("workouts.index"))
    return render_template("workouts/form.html", form=form, title="Dodaj trening")


@bp.route("/<int:workout_id>/edit", methods=["GET", "POST"])
@login_required
def edit(workout_id):
    workout = _get_own_workout_or_404(workout_id)
    form = WorkoutForm(obj=workout)
    if form.validate_on_submit():
        _fill_workout(workout, form)
        db.session.commit()
        flash("Zmiany zostały zapisane.", "success")
        return redirect(url_for("workouts.index"))
    return render_template("workouts/form.html", form=form, title="Edytuj trening")


@bp.route("/<int:workout_id>/delete", methods=["POST"])
@login_required
def delete(workout_id):
    workout = _get_own_workout_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    flash("Trening został usunięty.", "info")
    return redirect(url_for("workouts.index"))