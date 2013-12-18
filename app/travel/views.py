from flask import render_template, request, flash, redirect, url_for, jsonify

from travel import app
from forms import CountryForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CountryForm(request.form)
    if request.method == 'POST' and form.validate():
        country = form.country.data
        form = CountryForm()
    return render_template('index.html', form=form)

def get_country_info():
    pass

