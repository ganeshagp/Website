from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, IntegerField, SelectField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskpage.models import Developer, Client


class DeveloperForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    username=StringField('Username',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    phone_number = StringField('Phone Number',validators=[DataRequired()])
    domain = SelectField('Domain', choices=['Web Developer','Graphics Designer','Digital Marketing','Video Editing'], validators=[DataRequired()])
    github_link = StringField('Github Link', validators=[DataRequired()])
    linkedin_link = StringField('Linkedin Link', validators=[DataRequired()])
    experience = StringField('Experience', validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_phone_number(self, phone_number):
        dev = Developer.query.filter_by(phone_number=phone_number.data).first()
        if dev:
            raise ValidationError('That phone number is taken. Please choose a different one.')
            
    def validate_username(self, username):
        dev = Developer.query.filter_by(username=username.data).first()
        if dev:
            raise ValidationError('That username is taken. Please choose a different one.')

class ClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    username=StringField('Username',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()],)
    confirm_password= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_phone_number(self, phone_number):
        client = Client.query.filter_by(phone_number=phone_number.data).first()
        if client:
            raise ValidationError('That phone number is taken. Please choose a different one.')
            
    
    def validate_username(self, username):
        client = Client.query.filter_by(username=username.data).first()
        if client:
            raise ValidationError('That username is taken. Please choose a different one.')
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')  
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    account_type = SelectField('Account Type', choices=['Developer','Client'], validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_phone_number(self, phone_number):
        if phone_number.data != current_user.phone_number:
            if current_user.account_type == 'Developer':
                user = Developer.query.filter_by(phone_number=phone_number.data).first()
                if user:
                    raise ValidationError('That phone number is taken. Please choose a different one.')
            else:
                user = Client.query.filter_by(phone_number=phone_number.data).first()
                if user:
                    raise ValidationError('That phone number is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            if current_user.account_type == 'Developer':
                user = Developer.query.filter_by(email=email.data).first()
                if user:
                    raise ValidationError('That email is taken. Please choose a different one.')
            else:
                user = Client.query.filter_by(email=email.data).first()
                if user:
                    raise ValidationError('That email is taken. Please choose a different one.')
                
    def validate_username(self, username):
        if username.data != current_user.username:
            if current_user.account_type == 'Developer':
                user = Developer.query.filter_by(username=username.data).first()
                if user:
                    raise ValidationError('That username is taken. Please choose a different one.')
            else:
                user = Client.query.filter_by(username=username.data).first()
                if user:
                    raise ValidationError('That username is taken. Please choose a different one.')
