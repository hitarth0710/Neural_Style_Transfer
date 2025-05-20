from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange
from flask_wtf import FlaskForm



class StyleTransferIndexForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Start Style Transfer')


class StyleTransferForm(FlaskForm):
    content_image = FileField('Content Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    style_image = FileField('Style Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    # Add the style_prompt field
    style_prompt = TextAreaField('Style Prompt', validators=[Optional()])

    # Add the style_strength field
    style_strength = FloatField('Style Strength (0.1-1.0)', validators=[
        Optional(),
        NumberRange(min=0.1, max=1.0, message='Value must be between 0.1 and 1.0')
    ], default=0.75)

    submit = SubmitField('Transfer Style')

