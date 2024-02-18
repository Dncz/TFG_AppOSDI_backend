from SPARQLWrapper import SPARQLWrapper, JSON
from pandas import json_normalize
from config import FUSEKI_URL, PREFIXES
from owlready2 import *
from rdflib import Graph

import json

# URL del endpoint SPARQL de tu servidor Jena Fuseki
# fuseki_endpoint = "http://localhost:3030/OSDI_dataset/query"

# Configuración del objeto SPARQLWrapper
sparql = SPARQLWrapper(FUSEKI_URL)
sparql.setReturnFormat(JSON)

def get_information():
  # Configuración del objeto SPARQLWrapper
  # sparql = SPARQLWrapper(FUSEKI_URL)
  # sparql.setReturnFormat(JSON)

  # Ejemplo de consulta SPARQL
  query = PREFIXES + """
    SELECT ?ontology ?versionIRI ?comment
    WHERE {
      ?ontology rdf:type owl:Ontology .
      OPTIONAL { ?ontology owl:versionIRI ?versionIRI . }
      OPTIONAL { ?ontology rdfs:comment ?comment . }
    }
  """

  sparql.setQuery(query)
  ret = sparql.queryAndConvert()
  ret = json_normalize(ret['results']['bindings'])
  print(ret)
  
  # for r in ret['results']['bindings']:
  #     print(r)

def get_classes():

  query = PREFIXES + """
    SELECT ?x ?className ?comment
    WHERE {
      ?x rdf:type owl:Class .
      OPTIONAL { ?x rdfs:label ?label . }
      BIND(STRAFTER(STR(?x), "#") AS ?className)
      OPTIONAL { ?x rdfs:comment ?comment . }
    }
  """

  sparql.setQuery(query)
  ret = sparql.queryAndConvert()
  
  # print(ret)
  # print("\n")
  
  results_json = []
  for r in ret['results']['bindings']:
    if not r['x']['value'].startswith('b'):
      results_json.append({
        "IRI": r['x']['value'],
        "className": r['className']['value'],
        'comment': r['comment']['value'] if 'comment' in r else ''
      })
  
  json_string = json.dumps(results_json, indent=2)
  print(json_string + "\n Total: " + str(json_string.count('className')) + " clases")


def get_form_data_properties():
  
  # obtiene el nombre de la clase, dataproperties asociados y sus IRIs de los dataproperties
  query = PREFIXES +  """ 
    SELECT DISTINCT ?class ?className 
                    (GROUP_CONCAT(?dataTypeProperty; separator=", ") AS ?dataTypePropertiesIRIs)
                    (GROUP_CONCAT(?dataTypePropertyName; separator=", ") AS ?dataTypeProperties)
    WHERE {
      ?class rdf:type owl:Class .
      ?dataTypeProperty rdf:type owl:DatatypeProperty .
      ?class rdfs:subClassOf* ?parentClass .
      ?parentClass owl:onProperty ?dataTypeProperty .
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
      "dataTypeProperties": r['dataTypeProperties']['value']
    })
  
  json_string = json.dumps(results_json, indent=2)
  print(json_string)
  
  
# TODO: en la anterior función tengo cada calse con sus dataproperties para una parte del fomrulario
# entonces, tengo que añadir sus restricciones a esas dataporioerties
# TODO: hacer una pequeña prueba de mandar los nombres de las clases y crear un formulario con dos
# campos pequeño se nombre y descripción

def get_data_property(property):
  query = PREFIXES + """
    
  """