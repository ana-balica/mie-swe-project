import sys
import os
import csv

sys.path.append(os.getcwd())
from triplifier import env


class GDPTriplifier(object):
    def __init__(self, source_file_path):
        self.source_file_path = source_file_path
        self.data = None

    def triplify(self):
        countries = {}
        years = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013]
        with open(self.source_file_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for i, row in enumerate(reader):
                if i != 0:
                    country_name = row[2]
                    gdp_data = []
                    offset = 4
                    for i, year in enumerate(years):
                        gdp_value = row[i+offset]
                        if gdp_value:
                            gdp_data.extend([{year: row[i+offset]}])
                    countries[country_name] = gdp_data
        self.data = countries

    def render_template(self):
        if self.data is None:
            raise TypeError("First triplify the data, then try to render the rdf/turtle file")
        global env
        template = env.get_template('gdp_template.ttl')
        return template.render(countries=self.data)
        


if __name__ == "__main__":
    pwd = os.getcwd()
    gdp = GDPTriplifier(os.path.join(pwd, 'cache/gdp.csv'))
    gdp.triplify()
    ttl_data = gdp.render_template()
    with open(os.path.join(pwd, 'output/gdp.ttl'), "w") as f:
        f.write(ttl_data)