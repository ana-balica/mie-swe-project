import sys
import os
import csv
import re

sys.path.append(os.getcwd())
from triplifier import env


class AirportTriplifier(object):
    """ Custom triplifier class - converts from csv to ttl (turtle format)
    """
    def __init__(self, source_file_path):
        """ Class initializer

        @param source_file_path: path to the csv file to be converted
        """
        self.source_file_path = source_file_path

    def triplify(self):
        """ Convert csv data to turtle format

        @return: dict of dicts of the format {airport_name: {"icao": ICAO, "country": country,
                 "faa": FAA,  "long": longitude, "lat": latitude, "alt": altitude }
        """
        airports = {}
        with open(self.source_file_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for i, row in enumerate(reader):
                if i != 0:
                    # even if it says that data is encoded to latin-1, it actually
                    # contains a lot of unicode characters
                    airport_name = re.sub('[\s,\.\(\)\'/\\\]', '_', row[1]).decode('utf-8')
                    country = re.sub('[\s,\.\(\)\']', '_', row[3])
                    location, icao = row[4], row[5]
                    lat, long, alt = row[6], row[7], row[8]
                    airports_data = dict(country=country,
                                         icao=icao,
                                         lat=lat,
                                         long=long,
                                         alt=alt)
                    if country == "United_States":
                        airports_data["faa"] = location
                    else:
                        airports_data["iata"] = location
                    airports[airport_name] = {}
                    for key, value in airports_data.iteritems():
                        if value and value != "\\N":
                            airports[airport_name].update({key: value})
        return airports

    def render_template(self, template_name, data):
        """ Render the template to output a file in ttl format

        @param data: data structure containing infomation about airports
        @rtype: string
        @return: turtle formated data
        """
        if data is None:
            raise TypeError("First triplify the data, then try to render the rdf/turtle file")
        template = env.get_template(template_name)
        return template.render(airports=data)


if __name__ == "__main__":
    pwd = os.getcwd()
    airport_tp = AirportTriplifier(os.path.join(pwd, 'cache/airports.csv'))
    data = airport_tp.triplify()
    airport_ttl_data = airport_tp.render_template('airports_template.ttl', data)
    with open(os.path.join(pwd, 'output/airports.ttl'), "w") as f:
        f.write(airport_ttl_data.encode('utf-8'))
