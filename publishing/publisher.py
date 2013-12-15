import os
import sys
import rdflib

from jinja2 import FileSystemLoader, Environment


pwd = os.getcwd()
template_dir = os.path.join(pwd, 'templates/')
env = Environment(loader=FileSystemLoader(template_dir))


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
        @return: set of results tuples
        """
        qres = self.g.query(query)
        result = []
        for row in qres:
            result.append(tuple([item.toPython() for item in row]))
        return result


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
        f.write(output)


if __name__ == "__main__":
    pwd = os.getcwd()
    extractor = Extractor()

    # === Countries ==== #
    queries = []
    query.append("""SELECT ?country_name ?country_code
               WHERE {
               ?country_object gn:name ?country_name .
               ?country_object gn:countryCode ?country_code .
            }""")

    extractor.parse_graph(os.path.join(pwd, "../download/output/gdp.ttl"))
    res = extractor.extract_items(query)
    publish("rdfa_country.html", os.path.join(pwd, 'rdfa/rdfa_country.html'), dict(countries=res))

    # === GDP ==== #
