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

from metrologist.microscopes.models import Microscope, Objective, Modality


class NewObjectiveForm(FlaskForm):

    name = StringField("Objective name")
    lensNA = FloatField("Numerical aperture")
    magnification = IntegerField("Magnification")

    def create(self):
        new = Objective(
            name=self.name.data,
            lensNA=self.lensNA.data,
            magnification=self.magnification.data,
        )
        return new


class NewMicroscopeForm(FlaskForm):

    name = StringField("Microscope name")
    modality = StringField("Modality")
    objectives = FieldList(SelectField)
    add_objective = SubmitField("add an objective", render_kw={"class": "btn btn-info"})
    del_objective = SubmitField(
        "remove last objective", render_kw={"class": "btn btn-info"}
    )
    save = SubmitField("save", render_kw={"class": "btn btn-light"})
    cancel = SubmitField("Cancel", render_kw={"class": "btn btn-light"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_choices(self, **filter_by_kwargs):
        self.modality.choices = [(0, "-")] + [
            (modality.id, modality.name)
            for modality in Modality.query.filter_by(**filter_by_kwargs)
        ]
        for objective in self.objectives.entries:
            objective.choices = [(0, "-")] + [
                (obj.id, str(obj))
                for obj in Objective.query.filter_by(**filter_by_kwargs)
            ]

    def create_microscope(self):
        new = Microscope(
            name=self.name.data,
            modality_id=self.modality.data,
            objectives=[obj.id for obj in self.objectives.entries],
        )
        new.save
        return new
