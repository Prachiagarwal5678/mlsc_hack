from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Hackathon.models import User, ParkingLot

class RegisterationForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	company = StringField('Company Name', validators=[DataRequired()])
	submit = SubmitField('Sign Up')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Sorry this email is taken, Please choose another one')

class AddSlotForm(FlaskForm):
	level = StringField('Level', validators=[DataRequired()])
	slot_no = StringField('Slot No.', validators=[DataRequired()])
	parked = BooleanField('Parked')
	company = StringField('Company Name', validators=[DataRequired()])
	submit = SubmitField('Add Slot')

	def validate_email(self, slot_no):
		user = ParkingLot.query.filter_by(slot_no=slot_no.data).first()
		if user:
			raise ValidationError('Sorry this slot_no is taken, Please choose another one')

class SelectSlotForm(FlaskForm):
	submit = SubmitField('Find Slot')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
