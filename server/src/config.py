# Variables de entorno
#
# En el archivo server/src/config.py se encuentran las variables de entorno que se utilizan en el servidor.
#

FUSEKI_URL = "http://localhost:3030/OSDI_dataset3/query"
FUSEKI_UPDATE = "http://localhost:3030/OSDI_dataset3/update"

PREFIXES = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX ont: <http://www.ull.es/iis/simulation/ontologies/disease-simulation#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xml: <http://www.w3.org/XML/1998/namespace/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  """