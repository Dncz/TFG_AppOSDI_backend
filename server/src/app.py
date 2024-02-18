from SPARQLWrapper import SPARQLWrapper, JSON
from pandas import json_normalize
from config import FUSEKI_URL, PREFIXES
from owlready2 import *
from rdflib import Graph

import json

from flask import Flask

# URL del endpoint SPARQL de tu servidor Jena Fuseki
# fuseki_endpoint = "http://localhost:3030/OSDI_dataset/query"

# Configuración del objeto SPARQLWrapper
sparql = SPARQLWrapper(FUSEKI_URL)
sparql.setReturnFormat(JSON)


app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_form_data_properties():
  
  # obtiene el nombre de la clase, dataproperties asociados y sus IRIs de los dataproperties
  query = PREFIXES +  """ 
    SELECT DISTINCT ?class ?className 
                    (GROUP_CONCAT(?dataTypeProperty; separator=", ") AS ?dataTypePropertiesIRIs)
                    (GROUP_CONCAT(?dataTypePropertyName; separator=", ") AS ?dataTypeProperties)
                    (SAMPLE(?comment) AS ?comentario)
    WHERE {
      ?class rdf:type owl:Class .
      ?dataTypeProperty rdf:type owl:DatatypeProperty .
      ?class rdfs:subClassOf* ?parentClass .
      ?parentClass owl:onProperty ?dataTypeProperty .
      OPTIONAL { ?class rdfs:comment ?comment }
      BIND(strafter(str(?dataTypeProperty), "#") AS ?dataTypePropertyName)
      BIND(strafter(str(?class), "#") AS ?className)
    }
    GROUP BY ?class ?className
  """
  
  sparql.setQuery(query)
  ret = sparql.queryAndConvert()
  
  results_json = []
  for r in ret['results']['bindings']:
    results_json.append({
      "class": r['class']['value'],
      "className": r['className']['value'], 
      "dataTypePropertiesIRIs": r['dataTypePropertiesIRIs']['value'],
      "dataTypeProperties": r['dataTypeProperties']['value'],
      "comentario": r['comentario']['value'] if 'comentario' in r else ""
    })
  
  json_string = json.dumps(results_json, indent=2)
  print(json_string)
  if len(json_string) > 0:
    return json_string
  else:
    return "No se encontraron resultados"
  
if __name__ == "__main__":
  app.run(debug=True)

# from endpoints import get_classes, get_form_data_properties

# if __name__ == "__main__":
    
#     print("función de prueba:\n")
#     # get_information()
#     # get_classes()
    
#     print("\n")
    
#     get_form_data_properties()