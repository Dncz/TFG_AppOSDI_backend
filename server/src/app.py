from SPARQLWrapper import SPARQLWrapper, JSON
from pandas import json_normalize
from config import FUSEKI_URL, PREFIXES
from owlready2 import *
from rdflib import Graph
from flask_cors import CORS

import json

from flask import Flask, jsonify

# URL del endpoint SPARQL de tu servidor Jena Fuseki
# fuseki_endpoint = "http://localhost:3030/OSDI_dataset/query"

# Configuración del objeto SPARQLWrapper
sparql = SPARQLWrapper(FUSEKI_URL)
sparql.setReturnFormat(JSON)


app = Flask(__name__)
CORS(app, origins=["http://localhost:4200"], methods=["GET"])

@app.route('/objectProperties/<path:class_Name>', methods=['GET'])
def get_object_properties(class_Name):
  # TODO: manejar excepciones
  try:
    ontology_IRI = "http://www.ull.es/iis/simulation/ontologies/disease-simulation#"
    total_IRI = ontology_IRI + class_Name

    query = PREFIXES + f"""
    SELECT DISTINCT ?objectProperty ?range ?objectPropertyName ?rangeName
    WHERE {{
      <{total_IRI}> rdf:type owl:Class .
      ?objectProperty rdf:type owl:ObjectProperty .
      <{total_IRI}> rdfs:subClassOf* ?parentClass .
      ?parentClass owl:onProperty ?objectProperty .
    
      ?objectProperty rdfs:range ?range .		# descarto las objectProperties que no tienen rango
      # TODO: fix some data with value in range blank nodes
      FILTER (isURI(?range))  # Filter for IRIs (URIs with names) only
      BIND(strafter(str(?objectProperty), "#") AS ?objectPropertyName)
      BIND(strafter(str(?range), "#") AS ?rangeName)
    }}
    GROUP BY ?objectProperty ?range ?objectPropertyName ?rangeName
    """
    
    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    results_json = []
    for r in ret['results']['bindings']:
      results_json.append({
        "IRI": r['objectProperty']['value'],
        "name": r['objectPropertyName']['value'],
        "rangeIRI": r['range']['value'],
        "rangeName": r['rangeName']['value']
      })
    
    json_string = json.dumps(results_json, indent=2)
    print(json_string)
    if len(json_string) > 0:
      return json_string
    else:
      return "No se encontraron resultados"
  except ValueError as e:
    return jsonify({"error": str(e)}), 400

@app.route('/dataProperties/<path:class_IRI>', methods=['GET'])
def get_dataproperties(class_IRI):
  ontology_IRI = "http://www.ull.es/iis/simulation/ontologies/disease-simulation#"
  total_IRI = ontology_IRI + class_IRI

  query = PREFIXES + f"""
  SELECT DISTINCT ?className ?about 
                  (GROUP_CONCAT(?dataTypeProperty; separator=", ") AS ?dataTypePropertiesIRIs)
                  (GROUP_CONCAT(?dataTypePropertyName; separator=", ") AS ?dataTypeProperties)
                  (SAMPLE(?comment) AS ?comentario)
  WHERE {{
    <{total_IRI}> rdf:type owl:Class .
    ?dataTypeProperty rdf:type owl:DatatypeProperty .
    <{total_IRI}> rdfs:subClassOf* ?parentClass .
    ?parentClass owl:onProperty ?dataTypeProperty .
    <{total_IRI}> rdf:about ?about .
    OPTIONAL {{ <{total_IRI}> rdfs:comment ?comment }}
    BIND(strafter(str(?dataTypeProperty), "#") AS ?dataTypePropertyName)
    BIND(strafter(str(<{total_IRI}>), "#") AS ?className)
  }}
  GROUP BY ?class ?className ?about
  """
  
  sparql.setQuery(query)
  ret = sparql.queryAndConvert()
  
  results_json = {}
  for r in ret['results']['bindings']:
    results_json = {
      "classIRI": total_IRI,
      "className": r['className']['value'], 
      "dataTypePropertiesIRIs": r['dataTypePropertiesIRIs']['value'],
      "dataTypeProperties": r['dataTypeProperties']['value'],
      "comentario": r['comentario']['value'] if 'comentario' in r else "",
      "clasification": r['about']['value']
    }
  
  json_string = json.dumps(results_json, indent=2)
  print(json_string)
  if len(json_string) > 0:
    return json_string
  else:
    return "No se encontraron resultados"

@app.route('/classes/<path:class_Name>', methods=['GET'])
def get_class(class_Name):
  ontology_IRI = "http://www.ull.es/iis/simulation/ontologies/disease-simulation#"
  total_IRI = ontology_IRI + class_Name
  
  query = PREFIXES + f"""
  SELECT DISTINCT ?class ?className ?about
                  (SAMPLE(?comment) AS ?comentario)
  WHERE {{
    ?class rdf:type owl:Class .
    ?class rdf:about ?about .
    OPTIONAL {{ ?class rdfs:comment ?comment . }}
    BIND(strafter(str(?class), "#") AS ?className)
    FILTER (?class = <{total_IRI}>)
  }}
  GROUP BY ?class ?className ?about
  """
  
  sparql.setQuery(query)
  ret = sparql.queryAndConvert()
  
  results_json = {}
  for r in ret['results']['bindings']:
    results_json = {
      "classURI": r['class']['value'],
      "className": r['className']['value'], 
      "comentario": r['comentario']['value'] if 'comentario' in r else "",
      "clasification": r['about']['value']
    }
  
  json_string = json.dumps(results_json, indent=2)
  print(json_string)
  if len(json_string) > 0:
    return json_string
  else:
    return "No se encontraron resultados"

@app.route('/classes', methods=['GET'])
def get_classes():
  query = PREFIXES + """
  SELECT DISTINCT ?class ?className ?about
                  (SAMPLE(?comment) AS ?comentario)
  WHERE {
    ?class rdf:type owl:Class .
    # ?dataTypeProperty rdf:type owl:DatatypeProperty .
    # ?class rdfs:subClassOf* ?parentClass .
    # ?parentClass owl:onProperty ?dataTypeProperty .
    ?class rdf:about ?about .
    OPTIONAL { ?class rdfs:comment ?comment . }
    # BIND(strafter(str(?dataTypeProperty), "#") AS ?dataTypePropertyName)
    BIND(strafter(str(?class), "#") AS ?className)
  }
  GROUP BY ?class ?className ?about
  """
  
  sparql.setQuery(query)
  ret = sparql.queryAndConvert()
  
  print (ret)
  
  results_json = []
  for r in ret['results']['bindings']:
    results_json.append({
      "classURI": r['class']['value'],
      "className": r['className']['value'], 
      "comentario": r['comentario']['value'] if 'comentario' in r else "",
      "clasification": r['about']['value']
    })
  
  json_string = json.dumps(results_json, indent=2)
  print(json_string)
  if len(json_string) > 0:
    return json_string
  else:
    return "No se encontraron resultados"
  
@app.route('/restrictionDataProperty/<path:class_Name>/<path:class_Property>', methods=['GET'])
def get_restriction_dataproperty(class_Name, class_Property):
# def get_restriction_dataproperty():
  # classNameIRI = "http://www.ull.es/iis/simulation/ontologies/disease-simulation#" + "DataItemType"
  # "hasDescription, hasRefToDO, hasRefToGARD, hasRefToICD, hasRefToOMIM, hasRefToORDO, hasRefToSNOMED"
  # dataPropertyIRI = "http://www.ull.es/iis/simulation/ontologies/disease-simulation#" + "hasRefToSTATO"
  print("className:", class_Name)
  print("propertyName:", class_Property)

  
  classNameIRI = "http://www.ull.es/iis/simulation/ontologies/disease-simulation#" + class_Name
  dataPropertyIRI = "http://www.ull.es/iis/simulation/ontologies/disease-simulation#" + class_Property
  # TODO: hacer que esta consulta pueda servir para aquellas propiedades que tengan más de 2 restricciones
  query = PREFIXES + f"""
  SELECT DISTINCT ?restriction ?restrictionType ?restrictionValue ?restrictionTypeName
  WHERE {{
    ?class rdf:type owl:Class .
    ?class rdfs:subClassOf ?restriction .
    ?restriction owl:onProperty ?dataProperty .
    ?restriction ?restrictionType ?restrictionValue .
    FILTER (?class = <{classNameIRI}> && ?dataProperty = <{dataPropertyIRI}>)
    FILTER (?restrictionType IN (owl:someValuesFrom, owl:minQualifiedCardinality, owl:maxQualifiedCardinality))
    BIND(strafter(str(?restrictionType), "#") AS ?restrictionTypeName)
  }}
  GROUP BY ?restriction ?restrictionType ?restrictionValue ?restrictionTypeName
  """
  
  sparql.setQuery(query)
  ret = sparql.queryAndConvert()
  
  results_json = {}
  for r in ret['results']['bindings']:
    results_json = {
      "restriction": r['restriction']['value'],
      "restrictionType": r['restrictionType']['value'], 
      "restrictionValue": r['restrictionValue']['value'],
      "restrictionTypeName": r['restrictionTypeName']['value']
    }
  
  json_string = json.dumps(results_json, indent=2)
  print(json_string)
  if len(json_string) > 0:
    return json_string
  else:
    return "No se encontraron resultados"
  
# @app.route('/getPredicates/<path:class_name>', methods=['GET'])
# def get_predicates(class_name):
#   classNameIRI = "http://www.ull.es/iis/simulation/ontologies/disease-simulation#" + class_name
  
#   query = PREFIXES + f"""
#   SELECT ?objectProperty ?objectPropertyName ?range ?rangeName
#   WHERE {{
#     ?objectProperty rdf:type owl:ObjectProperty .
#     <{classNameIRI}>  rdfs:subClassOf* ?parentClass .
#     ?parentClass owl:onProperty ?objectProperty .
#     ?objectProperty rdfs:range ?range .
#     # TODO: fix some data with value in range blank nodes
#     FILTER (isURI(?range))  # Filter for IRIs (URIs with names) only
#     BIND(strafter(str(?objectProperty), "#") AS ?objectPropertyName)
# 		BIND(strafter(str(?range), "#") AS ?rangeName)
#   }}
#   """
  
#   sparql.setQuery(query)
#   ret = sparql.queryAndConvert()
  
#   results_json = []
#   for r in ret['results']['bindings']:
#     results_json.append({
#       "objectPropertyURI": r['objectProperty']['value'],
#       "objectPropertyName": r['objectPropertyName']['value'],
#       "rangeURI": r['range']['value'],
#       "rangeName": r['rangeName']['value'],
#     })
    
#   json_string = json.dumps(results_json, indent=2)
#   print(json_string)
#   if len(json_string) > 0:
#     return json_string
#   else:
#     return "No se encontraron resultados"
  
# TODO: en caso de que dos intancias tengan la misma description, pero diferente objectProperties
# qué dato escoger? o sea, puedo escoger un dato ya que son comunes, pero al hacer el create
# qué instancia pongo?
@app.route('/getIntances/<path:class_name>', methods=['GET'])
def get_intances(class_name):
  classNameIRI = "http://www.ull.es/iis/simulation/ontologies/disease-simulation#" + class_name
  
  query = PREFIXES + f"""
  # SELECT DISTINCT ?intanceIRI ?intanceName
  # WHERE {{
  #   ?intanceIRI rdf:type <{classNameIRI}> .
  #   BIND(strafter(str(?intanceIRI), "#") AS ?intanceName)
  # }}
  # GROUP BY ?intanceIRI ?intanceName
  
  SELECT DISTINCT ?intanceIRI ?intanceName ?description
  WHERE {{
    ?subclass rdfs:subClassOf* <{classNameIRI}> . #	buscamos las subclases de la clase principal
    ?intanceIRI rdf:type ?subclass . #  buscamos las intancias de las subclases
    OPTIONAL {{ ?intanceIRI <http://www.ull.es/iis/simulation/ontologies/disease-simulation#hasDescription> ?description . }}
    BIND(strafter(str(?intanceIRI), "#") AS ?intanceName)
    }}
  GROUP BY ?intanceIRI ?intanceName ?description
  """
  
  sparql.setQuery(query)
  ret = sparql.queryAndConvert()
  
  results_json = []
  for r in ret['results']['bindings']:
    results_json.append({
      "IRI": r['intanceIRI']['value'],
      "name": r['intanceName']['value'], 
      "description": r['description']['value'] if 'description' in r else "No description"
    })
    
  json_string = json.dumps(results_json, indent=2)
  print(json_string)
  if len(json_string) > 0:
    return json_string
  else:
    return "No se encontraron resultados"
  
# TODO: crear el endpoint de createInstance
  
if __name__ == "__main__":
  app.run(debug=True)