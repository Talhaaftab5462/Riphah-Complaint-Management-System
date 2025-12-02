from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired

class ComplaintForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    category = SelectField("Category", choices=[
        ("Academic", "Academic"),
        ("Facilities", "Facilities"),
        ("Transport", "Transport"),
        ("Hostel", "Hostel"),
        ("Administration", "Administration")
    ], validators=[DataRequired()])
    priority = SelectField("Priority", choices=[
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High")
    ], validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    attachment = FileField("Attachment")
