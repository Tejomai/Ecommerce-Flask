from wtforms import Form, BooleanField, StringField,IntegerField, PasswordField, validators,TextAreaField
from wtforms.fields.html5 import EmailField  

class SignupForm(Form):
    user_name = StringField('Username', [validators.Length(min=4, max=25), validators.DataRequired()])
    user_mail = EmailField('Mail Id', [validators.Length(min=6, max=30), validators.Email(), validators.DataRequired()])
    user_paswd = PasswordField('New Password', [ validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', [ validators.DataRequired()])

class LoginForm(Form):
    user_mail = EmailField('Mail Id', [validators.Length(min=6, max=30), validators.Email(), validators.DataRequired()])
    user_paswd = PasswordField('Password', [validators.DataRequired()])

class AddForm(Form):
    product_name = StringField("Product Name", [validators.DataRequired()])
    product_cost = IntegerField("Product Cost",[validators.DataRequired()])
    product_desc = TextAreaField("Product Description", [validators.DataRequired()])