from SPARQLWrapper import SPARQLWrapper, JSON
# from pandas import json_normalize
from config import FUSEKI_URL, PREFIXES, FUSEKI_UPDATE
# from owlready2 import *
# from rdflib import Graph
from flask_cors import CORS

import json

from flask import Flask, jsonify, request

# URL del endpoint SPARQL de tu servidor Jena Fuseki
# fuseki_endpoint = "http://localhost:3030/OSDI_dataset/query"

# Configuración del objeto SPARQLWrapper
sparql = SPARQLWrapper(FUSEKI_URL)
sparql.setReturnFormat(JSON)


app = Flask(__name__)
CORS(app, origins=["http://localhost:4200"], methods=["GET"])

# TODO: cambiar en el frontend el nombre de la clase por la IRI, así es más sencillo hacer la consulta
# TODO: cambiar las rutas de los endpoints para que sean más sencillos
# class/get/objectProperties/{className}
# class/get/dataProperties/{className}
# /dataProperty/get/restictions/{className}
# class/get/instances/{className}

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
  # TODO: arrreglar para que esta consulta sea más simple
  # obtener sólo el IRI y name de la dataProperty
  query = PREFIXES + f"""

  SELECT DISTINCT ?className 
                  (GROUP_CONCAT(?dataTypeProperty; separator=", ") AS ?dataTypePropertiesIRIs)
                  (GROUP_CONCAT(?dataTypePropertyName; separator=", ") AS ?dataTypePropertiesNames)
  WHERE {{
    <{total_IRI}> rdf:type owl:Class .
    ?dataTypeProperty rdf:type owl:DatatypeProperty .
    <{total_IRI}> rdfs:subClassOf* ?parentClass .
    ?parentClass owl:onProperty ?dataTypeProperty .
    BIND(strafter(str(?dataTypeProperty), "#") AS ?dataTypePropertyName)
    BIND(strafter(str(<{total_IRI}>), "#") AS ?className)
  }}
  GROUP BY ?className
  """
  # query = PREFIXES + f"""
  # SELECT DISTINCT ?dataTypePropertyName ?dataTypePropertyIRI
  # WHERE {{
  #     <{total_IRI}> rdf:type owl:Class .
  #     ?dataTypePropertyIRI rdf:type owl:DatatypeProperty .
  #     <{total_IRI}> rdfs:subClassOf* ?parentClass .
  #     ?parentClass owl:onProperty ?dataTypePropertyIRI .
  #     BIND(strafter(str(?dataTypePropertyIRI), "#") AS ?dataTypePropertyName)
  #   }}
  # GROUP BY ?dataTypePropertyName ?dataTypePropertyIRI
  # """
  
  sparql.setQuery(query)
  ret = sparql.queryAndConvert()
  
  results_json = {}
  for r in ret['results']['bindings']:
    results_json = {
      "className": r['className']['value'],
      "IRIs": r['dataTypePropertiesIRIs']['value'],
      "names": r['dataTypePropertiesNames']['value']
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
  # FIX: - hacer que esta consulta pueda servir para aquellas propiedades que tengan más de 2 restricciones
  # query = PREFIXES + f"""
  # SELECT DISTINCT ?restriction ?restrictionType ?restrictionValue ?restrictionTypeName
  # WHERE {{
  #   ?class rdf:type owl:Class .
  #   ?class rdfs:subClassOf ?restriction .
  #   ?restriction owl:onProperty ?dataProperty .
  #   ?restriction ?restrictionType ?restrictionValue .
  #   FILTER (?class = <{classNameIRI}> && ?dataProperty = <{dataPropertyIRI}>)
  #   FILTER (?restrictionType IN (owl:someValuesFrom, owl:minQualifiedCardinality, owl:maxQualifiedCardinality))
  #   BIND(strafter(str(?restrictionType), "#") AS ?restrictionTypeName)
  # }}
  # GROUP BY ?restriction ?restrictionType ?restrictionValue ?restrictionTypeName
  # """
  
  # TODO: cambiar a esta query y ajustar la estructura de datos en el frontend
  query = PREFIXES + f"""
  SELECT DISTINCT ?restriction ?restrictionType ?restrictionValue ?restrictionTypeName
  WHERE {{
    ?class rdf:type owl:Class .
    ?class rdfs:subClassOf* ?restriction .
    ?restriction owl:onProperty ?dataProperty .
    ?restriction ?restrictionType ?restrictionValue .
    FILTER (?class = <{classNameIRI}> && ?dataProperty = <{dataPropertyIRI}>)
    BIND(strafter(str(?restrictionType), "#") AS ?restrictionTypeName)
  }}
  GROUP BY ?restriction ?restrictionType ?restrictionValue ?restrictionTypeName
  """
  
  sparql.setQuery(query)
  ret = sparql.queryAndConvert()
  
  results_json = []
  for r in ret['results']['bindings']:
    results_json.append({
      "typeIRI": r['restrictionType']['value'], 
      "valueIRI": r['restrictionValue']['value'],
      "typeName": r['restrictionTypeName']['value']
    })
  
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
  # SELECT DISTINCT ?intanceIRI ?intanceName ?label
  # WHERE {{
  #   ?intanceIRI rdf:type <{classNameIRI}> .
  #   BIND(strafter(str(?intanceIRI), "#") AS ?intanceName)
  # }}
  # GROUP BY ?intanceIRI ?intanceName
  
  SELECT DISTINCT ?intanceIRI ?intanceName ?description ?label
  WHERE {{
    ?subclass rdfs:subClassOf* <{classNameIRI}> . #	buscamos las subclases de la clase principal
    ?intanceIRI rdf:type ?subclass . #  buscamos las intancias de las subclases
    OPTIONAL {{ ?intanceIRI <http://www.ull.es/iis/simulation/ontologies/disease-simulation#hasDescription> ?description . }}
    OPTIONAL {{
    	?intanceIRI rdfs:label ?label.
  	}}
    BIND(strafter(str(?intanceIRI), "#") AS ?intanceName)
    }}
  GROUP BY ?intanceIRI ?intanceName ?description ?label
  """
  
  sparql.setQuery(query)
  ret = sparql.queryAndConvert()
  
  results_json = []
  for r in ret['results']['bindings']:
    results_json.append({
      "IRI": r['intanceIRI']['value'],
      "name": r['intanceName']['value'],
      "description": r['description']['value'] if 'description' in r else "No description",
      "label": r['label']['value'] if 'label' in r else "No label"
    })
    
  json_string = json.dumps(results_json, indent=2)
  print(json_string)
  if len(json_string) > 0:
    return json_string
  else:
    return "No se encontraron resultados"
  
# TODO: crear el endpoint de createInstance
# sparqlUpdate = SPARQLWrapper(FUSEKI_UPDATE)
# sparqlUpdate.setReturnFormat(JSON)

# @app.route('/createInstance/<path:class_name>', methods=['POST'])
# def create_instance(class_name):
#   classNameIRI = "http://www.ull.es/iis/simulation/ontologies/disease-simulation#" + class_name
#   data = request.json
#   print(data)
#   if not data:
#     return jsonify({"error": "No data provided"}), 400
#   # data = {
#   #   "name": "instanceName",
#   #   "description": "description",
#   #   "objectProperties": [
#   #     {
#   #       "objectPropertyIRI": "http://www.ull.es/iis/simulation/ontologies/disease-simulation#hasRefToDO",
#   #       "objectProperty": "hasRefToDO",
#   #       "objectPropertyValue": "http://www.ull.es/iis/simulation/ontologies/disease-simulation#DOID_0050156"
#   #     }
#   #   ],
#   #   "dataProperties": [
#   #     {
#   #       "dataPropertyIRI": "http://www.ull.es/iis/simulation/ontologies/disease-simulation#hasDescription",
#   #       "dataProperty": "hasDescription",
#   #       "dataPropertyValue": "description"
#   #     }
#   #   ]
#   # }
  
#   # Crear la instancia
#   query = PREFIXES + f"""
#   INSERT DATA {{
#     <http://www.ull.es/iis/simulation/ontologies/disease-simulation#{data['name']}> rdf:type <{classNameIRI}> .
#     <http://www.ull.es/iis/simulation/ontologies/disease-simulation#{data['name']}> rdfs:label "{data['name']}" .
#     <http://www.ull.es/iis/simulation/ontologies/disease-simulation#{data['name']}> <http://www.ull.es/iis/simulation/ontologies/disease-simulation#hasDescription> "{data['description']}" .
#   }}
#   """
  
#   sparqlUpdate.setQuery(query)
#   ret = sparqlUpdate.query()
  
#   # Crear las objectProperties
#   for objectProperty in data['objectProperties']:
#     query = PREFIXES + f"""
#     INSERT DATA {{
#       <http://www.ull.es/iis/simulation/ontologies/disease-simulation#{data['name']}> <{objectProperty['objectPropertyIRI']}> <{objectProperty['objectPropertyValue']}> .
#     }}
#     """
      
  
if __name__ == "__main__":
  app.run(debug=True)