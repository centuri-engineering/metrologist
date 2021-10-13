import logging


from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    FloatField,
    IntegerField,
    SelectField,
    SubmitField,
    FieldList,
    FormField,
    TextAreaField,
)
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length

from metrologist.microscopes.models import Microscope, Objective, Instrument, Modality


class NewObjectiveForm(FlaskForm):

    name = StringField("Objective name")
    lenNA = FloatField("Numerical aperture")
    magnification = IntegerField("Magnification")


class NewMicroscopeForm(FlaskForm):

    name = StringField("Microscope name")
    modality = StringField("Modality")


class NewInstrumentForm(FlaskForm):
    name = StringField("Instrument name")
    microscope = SelectField("Microscope")
    objectives = FieldList(SelectField)
