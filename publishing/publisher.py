import os
import sys
import rdflib
from itertools import islice

from jinja2 import FileSystemLoader, Environment


pwd = os.getcwd()
template_dir = os.path.join(pwd, 'templates/')
env = Environment(loader=FileSystemLoader(template_dir))


# TODO: create a module and put Extractor to a single file
class Extractor(object):
    """ Wrapper around rdflib for extracting data from turtle files
    """

    def __init__(self):
        self.g = rdflib.Graph()

    def parse_graph(self, filename):
        self.g.parse(filename, format="turtle")

    def extract_items(self, query):
        """ Run the query and return results in Python format (strings, integers)

        @param query: a SPARQL query string (don't include prefixes)
        @return: generator of tuples containing the data
        """
        qres = self.g.query(query)
        for row in qres:
            yield tuple([item.toPython() for item in row])

    def get_size(self):
        return len(self.g)


def publish(template_name, output_file, data):
    """ Publish the results to a file

    @param template_name: name of the template that should be rendered from 
                          templates/ folder
    @param output_file: full path to the output file
    @param data: a dict with named params as keys and data as values
    """
    template = env.get_template(template_name)
    output = template.render(**data)
    with open(output_file, "w") as f:
        f.write(output.encode('utf-8'))

def split_iterator(iterator, size, delimiter):
    """ Helper function to split a generator into chuncks of generators

    @param iterator: an iterator
    @param size: total size of the iterator
    @param delimiter: the size of the final chuncks
    @return: list of iterators
    """
    iterables = []
    for i in xrange(0, size, delimiter):
        iterables.extend([islice(iterator, 0, delimiter)])
    return iterables


if __name__ == "__main__":
    pwd = os.getcwd()
    extractor = Extractor()

    queries, source_files = [], []
    template_names, output_files = [], []
    template_dicts = []

    # TODO: !!! organize the mess, split to files in the module, remove redundant copy-pasting !!!

    # === Country names and codes ==== #
    queries.append("""SELECT ?country_name ?country_code
        WHERE {
            ?country_object gn:name ?country_name .
            ?country_object gn:countryCode ?country_code .
        }""")
    source_files.append(os.path.join(pwd, "../download/output/gdp.ttl"))
    template_names.append("rdfa_countries.html")
    output_files.append(os.path.join(pwd, 'rdfa/rdfa_countries.html'))
    template_dicts.append(dict(countries=None))

    # === Country GDP in year yyyy ==== #
    queries.append("""SELECT ?country_name ?gdp ?year
        WHERE {
            ?country_object gn:name ?country_name .
            ?blank rdf:value ?gdp .
            ?blank ei:inYear ?year .
        }""")
    source_files.append(os.path.join(pwd, "../download/output/gdp.ttl"))
    template_names.append("rdfa_gdp.html")
    output_files.append(os.path.join(pwd, 'rdfa/rdfa_gdp.html'))
    template_dicts.append(dict(gdp_data=None))

    # === Country Tourism rate in year yyyy ==== #
    queries.append("""SELECT ?country_name ?tourists ?year
        WHERE {
            ?country_object gn:name ?country_name .
            ?blank rdf:value ?tourists .
            ?blank ei:inYear ?year .
        }""")
    source_files.append(os.path.join(pwd, "../download/output/tourism.ttl"))
    template_names.append("rdfa_tourism.html")
    output_files.append(os.path.join(pwd, 'rdfa/rdfa_tourism.html'))
    template_dicts.append(dict(gdp_data=None))

    # === Airport names ==== #
    queries.append("""SELECT ?airport_name ?airport_id ?iata
        WHERE {
            ?airport_object dc:title ?airport_name .
            ?airport_object dc:identifier ?airport_id .
            ?airport_object air:iataCode ?iata .
        }""")
    source_files.append(os.path.join(pwd, "../download/output/airports.ttl"))
    template_names.append("rdfa_airports.html")
    output_files.append(os.path.join(pwd, 'rdfa/rdfa_airports.html'))
    template_dicts.append(dict(airports=None))

    # === Airport location ==== #
    queries.append("""SELECT ?airport_name ?country ?long ?lat ?alt
        WHERE {
            ?airport_object a dbpedia-owl:Airport .
            ?airport_object dc:title ?airport_name .
            ?country_object a dbpedia-owl:country .
            ?country_object dc:title ?country .
            ?airport_object geo:longitude ?long .
            ?airport_object geo:latitude ?lat .
            ?airport_object geo:altitude ?alt .
        }""")
    source_files.append(os.path.join(pwd, "../download/output/airports.ttl"))
    template_names.append("rdfa_airports_location.html")
    output_files.append(os.path.join(pwd, 'rdfa/rdfa_airports_location.html'))
    template_dicts.append(dict(airports=None))

    # === Country names microformat ==== #
    queries.append("""SELECT ?country_name
        WHERE {
            ?country_object gn:name ?country_name .
        }""")
    source_files.append(os.path.join(pwd, "../download/output/gdp.ttl"))
    template_names.append("microformat_countries.html")
    output_files.append(os.path.join(pwd, 'microformats/microformat_countries.html'))
    template_dicts.append(dict(countries=None))

    # === Geo location microformat ==== #
    queries.append("""SELECT ?long ?lat ?alt
        WHERE {
            ?airport_object geo:longitude ?long .
            ?airport_object geo:latitude ?lat .
            ?airport_object geo:altitude ?alt .
        }""")
    source_files.append(os.path.join(pwd, "../download/output/airports.ttl"))
    template_names.append("microformat_geo.html")
    output_files.append(os.path.join(pwd, 'microformats/microformat_geo.html'))
    template_dicts.append(dict(positions=None))

    # === Country names and codes microdata === #
    queries.append("""SELECT ?country_name ?country_code
        WHERE {
            ?country_object gn:name ?country_name .
            ?country_object gn:countryCode ?country_code .
        }""")
    source_files.append(os.path.join(pwd, "../download/output/gdp.ttl"))
    template_names.append("microdata_countries.html")
    output_files.append(os.path.join(pwd, 'microdata/microdata_countries.html'))
    template_dicts.append(dict(countries=None))

    # === Airports microdata === #
    queries.append("""SELECT ?airport_name ?icao ?country ?long ?lat ?alt
        WHERE {
            ?airport_object a dbpedia-owl:Airport .
            ?airport_object dc:title ?airport_name .
            ?airport_object dc:identifier ?icao .
            ?country_object a dbpedia-owl:country .
            ?country_object dc:title ?country .
            ?airport_object geo:longitude ?long .
            ?airport_object geo:latitude ?lat .
            ?airport_object geo:altitude ?alt .
        }""")
    source_files.append(os.path.join(pwd, "../download/output/airports.ttl"))
    template_names.append("microdata_airports.html")
    output_files.append(os.path.join(pwd, 'microdata/microdata_airports.html'))
    template_dicts.append(dict(airports=None))

    for i, query in enumerate(queries):
        extractor.parse_graph(source_files[i])
        res = extractor.extract_items(query)
        result = islice(res, 0, 10000)
        for key, value in template_dicts[i].iteritems():
            template_dicts[i][key] = result
        publish(template_names[i], output_files[i], template_dicts[i])
