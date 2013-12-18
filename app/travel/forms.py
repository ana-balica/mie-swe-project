from wtforms import Form, TextField, SubmitField, validators


class CountryForm(Form):
    ''' The index page simple form for country search
    '''
    country = TextField('country', [validators.Length(min=1, max=50)])
    submit = SubmitField('search')
