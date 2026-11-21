from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager

DISCIPLINES = [
    ("swim", "Pływanie"),
    ("bike", "Rower"),
    ("run", "Bieganie"),
]
DISCIPLINE_LABELS = dict(DISCIPLINES)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    workouts = db.relationship(
        "Workout", backref="user", cascade="all, delete-orphan"
    )


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    discipline = db.Column(db.String(20), nullable=False, index=True)
    workout_date = db.Column(db.Date, nullable=False, index=True)
    duration_min = db.Column(db.Integer, nullable=False)
    distance_km = db.Column(db.Float, nullable=False)
    rpe = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    @property
    def discipline_label(self):
        return DISCIPLINE_LABELS.get(self.discipline, self.discipline)

    @property
    def duration_display(self):
        hours, minutes = divmod(self.duration_min, 60)
        return f"{hours} h {minutes:02d} min" if hours else f"{minutes} min"

    def __repr__(self):
        return f"<Workout {self.id} {self.discipline} {self.workout_date}>"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))