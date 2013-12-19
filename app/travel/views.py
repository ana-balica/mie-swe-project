import re
import json

from flask import render_template, request, flash, redirect, url_for, jsonify

from travel.models.models import *
from travel import app
from forms import CountryForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CountryForm(request.form)
    if request.method == 'POST' and form.validate():
        country = form.country.data
        form = CountryForm()
        return redirect(url_for('info', country_name=country))
        
    return render_template('index.html', form=form)


@app.route('/<country_name>')
def info(country_name):
    info = get_country_info(country_name)
    if not info:
            return render_template('no_info.html', country_name=country_name)
    else:
        airports, tourists, gdp = info
        return render_template('info.html', country_name=country_name, airports=airports,
            tourists=tourists, gdp=gdp)


def get_country_info(country_name):
    country_name = re.sub('[\s,\.\(\)\']', '_', country_name)
    airports = get_airports(country_name)
    tourists = get_tourists(country_name)
    gdp = get_gdp(country_name)
    if not airports and not tourists and not gdp:
        return None
    return airports, tourists, gdp



    

