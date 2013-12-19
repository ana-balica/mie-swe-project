import re

from flask import render_template, request, flash, redirect, url_for, jsonify

from travel.models.models import *

from travel import app
from forms import CountryForm

API_KEY = "AIzaSyBbF2-Rrsdr1CldjOEcf3M3qrxTyDCWtNI"


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CountryForm(request.form)
    if request.method == 'POST' and form.validate():
        country = form.country.data
        form = CountryForm()
        info = get_country_info(country)
        if not info:
            return render_template('no_info.html', country_name=country)
        else:
            airports, tourists, gdp = info
            print airports
            return render_template('info.html', country_name=country, airports=airports,
                tourists=tourists, gdp=gdp)
    return render_template('index.html', form=form)

@app.route('/no_info')
def no_info():
    return render

def get_country_info(country_name):
    country_name = re.sub('[\s,\.\(\)\']', '_', country_name)
    airports = get_airports(country_name)
    tourists = get_tourists(country_name)
    gdp = get_gdp(country_name)
    if not airports and not tourists and not gdp:
        return None
    return airports, tourists, gdp



    

