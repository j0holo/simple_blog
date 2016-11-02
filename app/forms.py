from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
	email = StringField([validators.Email()])
	password = PasswordField([validators.InputRequired()])
