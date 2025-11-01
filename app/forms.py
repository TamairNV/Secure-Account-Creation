from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
import re
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo




def validEmail(self, field):
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(EMAIL_REGEX,field.data):
        raise validators.ValidationError('Invalid Email format')
    domains = (".edu",".org",".ac.uk")

    if not field.data.endswith(domains):
        raise validators.ValidationError('Invalid Domain')




def checkPassword(self,field):
    special_characters = [
        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
        '-', '_', '+', '=', '[', ']', '{', '}', '|', '\\',
        ';', ':', '\'', '"', ',', '.', '<', '>', '/', '?',
        '`', '~'
    ]
    commonPasswords = [
        "password123",
        "admin",
        "123456",
        "qwerty",
        "letmein",
        "welcome",
        "iloveyou",
        "abc123",
        "monkey",
        "football"
    ]
    checks  = [False,False,False,False,False,False,False,False,False]
    errosBase = "Password must contain at least"
    errors = [f"{errosBase} one digit",
             f"{errosBase} one upper case character",
             f"{errosBase} one lower case character",
             f"{errosBase} one special character",
              f"Password must be at least 12 characters",
              f"Password must not contain username: {self.username.data}",
              f"Password must not contain email: {self.email.data}",
              f"Password must not contain whitespaces",
              f"Password is too common"
              ]
    password = field.data
    if len(password) >= 12:
        checks[4] = True
    if self.username.data not in password:
        checks[5] = True
    if self.email.data not in password:
        checks[6] = True

    if password not in commonPasswords:
        checks[8] = True

    if " " not in password:
        checks[7] = True
    for s in password:
        if s.isdigit():
            checks[0] = True

        if s.isupper():
            checks[1] = True

        if s.islower():
            checks[2] = True

        if s in special_characters:
            checks[3] = True

    shownErrors = []
    for i,c in enumerate(checks):

        if not c:
            shownErrors.append(errors[i])

    for error in shownErrors:
        raise validators.ValidationError(error)

def validUsername(self,field):
    username = field.data
    notAllowedNames = ["admin","root","superuser"]
    if username.lower() in notAllowedNames:
        raise validators.ValidationError('Username Not Allowed')
    pattern = r'^[a-zA-Z_]+$'

    if not re.fullmatch(pattern, username):
        raise validators.ValidationError('Invalid Username')



class Register(FlaskForm):
    username = StringField('Enter a Username',validators=[
            validators.InputRequired(),
            validUsername,
            Length(min=3,max=30, message='Username must be between 3 and 30 characters.')
        ])


    email = StringField('Enter an Email',validators=[validators.InputRequired(),validEmail])

    password = StringField('Enter a Password',
            validators=[
            validators.InputRequired(),
            checkPassword,
            Length(max=32, message='Password must be at least 12 characters long.'),
            EqualTo('confirmPassword', message='Passwords must match')
        ])

    confirmPassword = StringField("Confirm Password")

    bio = StringField('Enter your Bio')

    submit = SubmitField('Register')



