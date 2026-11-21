import datetime

from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    FloatField,
    IntegerField,
    SelectField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    NumberRange,
    Optional,
)

from ..models import DISCIPLINES


class CommaFloatField(FloatField):
    """FloatField, który przyjmuje zarówno 0.6, jak i 0,6."""

    def process_formdata(self, valuelist):
        if valuelist:
            valuelist = [valuelist[0].replace(",", ".")]
        super().process_formdata(valuelist)


class WorkoutForm(FlaskForm):
    discipline = SelectField(
        "Dyscyplina", choices=DISCIPLINES, validators=[DataRequired()]
    )
    workout_date = DateField(
        "Data",
        default=datetime.date.today,
        validators=[DataRequired(message="Podaj datę treningu.")],
    )
    duration_min = IntegerField(
        "Czas (minuty)",
        validators=[
            DataRequired(message="Podaj czas trwania."),
            NumberRange(min=1, max=1440, message="Czas musi mieścić się w 1-1440 min."),
        ],
    )
    distance_km = CommaFloatField(
        "Dystans (km)",
        validators=[
            InputRequired(message="Podaj dystans."),
            NumberRange(min=0.01, max=1000, message="Dystans musi mieścić się w 0,01-1000 km."),
        ],
        render_kw={"step": "0.01", "inputmode": "decimal"},
    )
    rpe = IntegerField(
        "RPE (1-10)",
        validators=[Optional(), NumberRange(min=1, max=10, message="RPE od 1 do 10.")],
    )
    notes = TextAreaField("Notatki", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Zapisz")