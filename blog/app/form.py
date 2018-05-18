from .models import User
from flask_wtf import Form
from wtforms import TextField, PasswordField, validators

class UserLoginForm(Form):
    name = TextField('Name', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            name=self.name.data).first()
        if user is None:
            self.name.errors.append('Unknown username')
            return False

        self.user = user
        return True


class PostForm(Form):
    title = TextField('Title', [validators.Required()])
    body = TextField('Body', [validators.Required()])

