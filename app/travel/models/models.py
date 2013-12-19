import logging
import StringIO
import requests
from lxml import etree

# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SPARQL endpoint
host = "http://localhost:8080/"


def get_query_result(query):
    data = { "query": query, "output": "text" }
    r = requests.post(host + "sparql/", data=data)

    if r.status_code != requests.codes.ok:   # something went wrong
        logging.warning("During the sparql request something went wrong. The response \
            status is {0}".format(r.status_code))
    return r.text

def extract_elements(contents):
    root = etree.XML(contents)
    tree = etree.ElementTree(root)
    elements = tree.xpath('//ns:binding/ns:literal', 
        namespaces={'ns': 'http://www.w3.org/2005/sparql-results#'})
    return elements


def get_airports(country_name):
    if not country_name:
        return

    query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

SELECT DISTINCT ?airport ?long ?lat
            WHERE {
                ?airport_obj a dbpedia-owl:Airport .
                ?airport_obj dc:title ?airport .
                ?airport_obj dc:coverage ?country_obj .
                ?country_obj dc:title "%s"^^xsd:string .
                ?airport_obj geo:longitude ?long .
                ?airport_obj geo:latitude ?lat .
            }""" % (country_name)

    result = get_query_result(query)
    elements = extract_elements(result)
    results = {}
    for i in range(len(elements))[::3]:
        results[elements[i].text] = {'long': elements[i+1].text, 'lat': elements[i+2].text}
    return results

def get_tourists(country_name):
    if not country_name:
        return

    query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX gn: <http://www.geonames.org/ontology#>
PREFIX ei: <http://www.economic_indicators.org/ontology/tourism#>

SELECT DISTINCT ?year ?value
            WHERE {
                ?country_obj gn:name "%s"^^xsd:string .
                ?country_obj ei:hasTouristsNr ?obj .
                ?obj rdf:value ?value .
            ?obj ei:inYear ?year .
            }
    """ % (country_name)

    result = get_query_result(query)
    elements = extract_elements(result)
    results = {}
    for i in range(len(elements))[::2]:
        results[elements[i].text] = elements[i+1].text
    return results

def get_gdp(country_name):
    if not country_name:
        return

    query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX gn: <http://www.geonames.org/ontology#>
PREFIX ei: <http://www.economic_indicators.org/ontology/gdp#>

SELECT DISTINCT ?year ?value
            WHERE {
                ?country_obj gn:name "%s"^^xsd:string .
                ?country_obj ei:hasGDP ?obj .
                ?obj rdf:value ?value .
            ?obj ei:inYear ?year .
            }
    """ % (country_name)

    result = get_query_result(query)
    elements = extract_elements(result)
    results = {}
    for i in range(len(elements))[::2]:
        results[elements[i].text] = elements[i+1].text
    return results



if __name__ == '__main__':
    get_airports("Moldova")
    get_tourists("Moldova")
    get_gdp("Moldova")

