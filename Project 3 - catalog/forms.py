from wtforms import Form, StringField, validators

class NewItem(Form):
	name = StringField('Name', validators = [validators.Length(min=4, max=25)])
	description = StringField('description', validators = [validators.Length(min=4, max=25)])


