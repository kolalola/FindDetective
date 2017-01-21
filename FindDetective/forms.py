from wtforms import Form, StringField, TextAreaField, validators, SelectField
from wtforms import HiddenField, PasswordField

strip_filter = lambda x: x.strip() if x else None

class BlogCreateForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    text = TextAreaField('Contents', [validators.Length(min=1)],
                         filters=[strip_filter])


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=255)],
                           filters=[strip_filter])
    password = PasswordField('Password', [validators.Length(min=3)])

    mail = StringField('Mail', [validators.Length(min=1, max=255)],
                           filters=[strip_filter])
    role= SelectField('Select',choices = [('Пользователь','User'),
                                          ('Детектив','Detective')])

class ProposeForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=11)],
                        filters=[strip_filter])
    description = TextAreaField('Contents', [validators.Length(min=1)],
                                filters=[strip_filter])
    phone = StringField('Phone', [validators.Length(min=1, max=11)],
                        filters=[strip_filter])
