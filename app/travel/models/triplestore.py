import os
import logging

from rdflib import Namespace, Literal, URIRef
from rdflib.graph import Graph, ConjunctiveGraph
from rdflib.plugins.memory import IOMemory


class Triplestore(object):
    """ Class representing a triplestore - a database for storage of triples
    """

    def __init__(self):
        """ Class initializer, creates a ConjunctiveGraph and initializes it with 
        the IOMemory storage
        """
        self.store = IOMemory()
        self.g = ConjunctiveGraph(store=self.store)

    def load_graphs(self, paths):
        """ Load all the available graphs to the ConjunctiveGraph

        @param paths: list of paths where from to extract turtle and rdf files and 
                      load to the store
        """
        format = None
        for path in paths:
            for root, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    if filename.endswith(".ttl"):
                        format = "turtle"
                    elif filename.endswith(".rdf"):
                        format = "application/rdf+xml"
                    if format is not None:
                        logging.info("Adding to the triplestore file '{0}'".format(filename))
                        g = Graph(store=self.store)
                        g.parse(os.path.join(root, filename), format=format)
                        format = None


if __name__ == "__main__":

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    datasets_path = os.path.join(root, '../../download/output')
    linksets_path_external = os.path.join(root, '../../linking/external')
    linksets_path_internal = os.path.join(root, '../../linking/internal')

    ts = Triplestore()
    ts.load_graphs([datasets_path, linksets_path_external, linksets_path_internal])
    ts.g.serialize(os.path.join(root, 'models/triplestore.ttl'), format='turtle')
