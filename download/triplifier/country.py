import sys
import os
import csv

sys.path.append(os.getcwd())
from triplifier import env


class CountryTriplifier(object):
    """ Custom triplifier class - converts from csv to ttl (turtle format)
    """
    def __init__(self, source_file_path):
        """ Class initializer

        @param source_file_path: path to the csv file to be converted
        """
        self.source_file_path = source_file_path

    def triplify(self):
        """ Convert csv data to turtle format

        @return: dict of dicts of the format {country_name: {country_code: code, 
                 year: value, another_year: value}, ]}
        """
        countries = {}
        years = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013]
        with open(self.source_file_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for i, row in enumerate(reader):
                if i != 0:
                    country_name = row[2]
                    country_code = row[3]
                    country_data = {}
                    country_data["country_code"] = country_code
                    offset = 4
                    for i, year in enumerate(years):
                        gdp_value = row[i+offset]
                        if gdp_value:
                            country_data[year] = row[i+offset]
                    countries[country_name] = country_data
        return countries

    def render_template(self, template_name, data):
        """ Render the template to output a file in ttl format

        @param data: data structure containing infomation about countries and gdp values
        @rtype: string
        @return: turtle formated data
        """
        if data is None:
            raise TypeError("First triplify the data, then try to render the rdf/turtle file")
        template = env.get_template(template_name)
        return template.render(countries=data)


if __name__ == "__main__":
    pwd = os.getcwd()
    gdp = CountryTriplifier(os.path.join(pwd, 'cache/gdp.csv'))
    data = gdp.triplify()
    gdp_ttl_data = gdp.render_template('gdp_template.ttl', data)
    with open(os.path.join(pwd, 'output/gdp.ttl'), "w") as f:
        f.write(gdp_ttl_data)

    tourism = CountryTriplifier(os.path.join(pwd, 'cache/tourism.csv'))
    data = tourism.triplify()
    tourism_ttl_data = tourism.render_template('tourism_template.ttl', data)
    with open(os.path.join(pwd, 'output/tourism.ttl'), 'w') as f:
        f.write(tourism_ttl_data)
