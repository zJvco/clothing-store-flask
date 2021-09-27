from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, RadioField
from wtforms.validators import Length, Email, DataRequired, EqualTo, Optional, ValidationError

from .models import User


class SigninForm(FlaskForm):
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign In")


class SignupForm(FlaskForm):
    username = StringField(label="Username", validators=[Length(min=4, max=50), DataRequired()])
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    gender = RadioField(label="Gender", validators=[DataRequired()], choices=[('male', 'Male'), ('female', 'Female'), ('undefined', 'Undefined')])
    phone = IntegerField(label="Number Phone", validators=[Optional()])
    password = PasswordField(label="Password", validators=[Length(min=6, max=128), DataRequired()])
    password_confirm = PasswordField(label="Confirm Password", validators=[EqualTo("password"), DataRequired()])
    submit = SubmitField(label="Sign Up")

    def validate_email(self, check_email):
        user = User.query.filter_by(email=check_email.data).first()
        if user:
            raise ValidationError("Email already exists")

    def validate_phone(self, check_phone):
        user = User.query.filter_by(phone=check_phone.data).first()
        if user:
            raise ValidationError("Phone already exists")


class AddressForm(FlaskForm):
    cep = StringField(label="CEP", validators=[Length(min=9, max=9), DataRequired()])
    street = StringField(label="Street", validators=[DataRequired()])
    number = IntegerField(label="Number", validators=[DataRequired()])
    city = StringField(label="City", validators=[DataRequired()])
    complement = StringField(label="Complement", validators=[Optional()])


class ProfileForm(FlaskForm):
    username = StringField(label="Username", validators=[Length(min=4, max=50), DataRequired()])
    email = StringField(label="Email")
    current_password = PasswordField(label="Current Password")
    password_new = PasswordField(label="Password", validators=[Length(min=6, max=128), Optional()])
    password_confirm = PasswordField(label="Confirm Password", validators=[EqualTo("password_new")])
    gender = RadioField(label="Gender", validators=[DataRequired()], choices=[('male', 'Male'), ('female', 'Female'), ('undefined', 'Undefined')])
    phone = IntegerField(label="Number Phone", validators=[Optional()])
    submit = SubmitField(label="Save Changes")
