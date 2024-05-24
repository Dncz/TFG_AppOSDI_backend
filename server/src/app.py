from SPARQLWrapper import SPARQLWrapper, JSON
from config import FUSEKI_URL, PREFIXES, FUSEKI_UPDATE
from flask_cors import CORS
import re
import json

from flask import Flask, jsonify, request

# Configuración del objeto SPARQLWrapper
sparql = SPARQLWrapper(FUSEKI_URL)
sparql.setReturnFormat(JSON)


app = Flask(__name__)
CORS(app, origins=["*"], methods=["GET", "POST"], supports_credentials=True)


@app.route('/objectProperties/<path:class_Name>', methods=['GET'])
def get_object_properties(class_Name):
  try:

    query = PREFIXES + f"""
    SELECT DISTINCT ?objectProperty ?range ?objectPropertyName ?rangeName
    WHERE {{
      ont:{class_Name} rdf:type owl:Class .
      ?objectProperty rdf:type owl:ObjectProperty .
      ont:{class_Name} rdfs:subClassOf* ?parentClass .
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

    if len(json_string) > 0:
      return json_string
    else:
      return jsonify({"error": "No se encontraron resultados", "status": 400}), 400
  except ValueError as e:
    return jsonify({"error": str(e), "status": 400}), 400

@app.route('/dataProperties/<path:class_Name>', methods=['GET'])
def get_dataproperties(class_Name):
  try:
    query = PREFIXES + f"""

    SELECT DISTINCT ?className 
                    (GROUP_CONCAT(?dataTypeProperty; separator=", ") AS ?dataTypePropertiesIRIs)
                    (GROUP_CONCAT(?dataTypePropertyName; separator=", ") AS ?dataTypePropertiesNames)
    WHERE {{
      ont:{class_Name} rdf:type owl:Class .
      ?dataTypeProperty rdf:type owl:DatatypeProperty .
      ont:{class_Name} rdfs:subClassOf* ?parentClass .
      ?parentClass owl:onProperty ?dataTypeProperty .
      BIND(strafter(str(?dataTypeProperty), "#") AS ?dataTypePropertyName)
      BIND(strafter(str(ont:{class_Name}), "#") AS ?className)
    }}
    GROUP BY ?className
    """
    
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

    if len(json_string) > 0:
      return json_string
    else:
      return jsonify({"error": "No se encontraron resultados", "status": 400}), 400
  except ValueError as e:
    return jsonify({"error": str(e), "status": 400}), 400

@app.route('/classes', methods=['GET'])
def get_classes():
  try:
    query = PREFIXES + """
    SELECT DISTINCT ?class ?className ?about
                    (SAMPLE(?comment) AS ?comentario)
    WHERE {
      ?class rdf:type owl:Class .
      ?class rdf:about ?about .
      OPTIONAL { ?class rdfs:comment ?comment . }
      # BIND(strafter(str(?dataTypeProperty), "#") AS ?dataTypePropertyName)
      BIND(strafter(str(?class), "#") AS ?className)
    }
    GROUP BY ?class ?className ?about
    """
    
    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
        
    results_json = []
    for r in ret['results']['bindings']:
      results_json.append({
        "classURI": r['class']['value'],
        "className": r['className']['value'], 
        "comentario": r['comentario']['value'] if 'comentario' in r else "",
        "clasification": r['about']['value']
      })
    
    json_string = json.dumps(results_json, indent=2)

    if len(json_string) > 0:
      return json_string
    else:
      return jsonify({"error": "No se encontraron resultados", "status": 400}), 400
  except ValueError as e:
    return jsonify({"error": str(e), "status": 400}), 400
  
@app.route('/restrictionDataProperty/<path:class_Name>/<path:data_Property_Name>', methods=['GET'])
def get_restriction_dataproperty(class_Name, data_Property_Name):
  try:
    query = PREFIXES + f"""
    SELECT DISTINCT ?restriction ?restrictionType ?restrictionValue ?restrictionTypeName
    WHERE {{
      ?class rdf:type owl:Class .
      ?class rdfs:subClassOf* ?restriction .
      ?restriction owl:onProperty ?dataProperty .
      ?restriction ?restrictionType ?restrictionValue .
      FILTER (?class = ont:{class_Name} && ?dataProperty = ont:{data_Property_Name})
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

    if len(json_string) > 0:
      return json_string
    else:
      return jsonify({"error": "No se encontraron resultados", "status": 400}), 400
  except ValueError as e:
    return jsonify({"error": str(e), "status": 400}), 400
  
@app.route('/getIntances/<path:class_name>', methods=['GET'])
def get_intances(class_name):
  try:
    query = PREFIXES + f"""  
    SELECT DISTINCT ?intanceIRI ?intanceName ?description ?label
    WHERE {{
      ?subclass rdfs:subClassOf* ont:{class_name} . #	buscamos las subclases de la clase principal
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

    if len(json_string) > 0:
      return json_string
    else:
      return jsonify({"error": "No se encontraron resultados", "status": 400}), 400
  except ValueError as e:
    return jsonify({"error": str(e), "status": 400}), 400


sparqlUpdate = SPARQLWrapper(FUSEKI_UPDATE)
sparqlUpdate.setReturnFormat(JSON)

@app.route('/createInstance/<path:class_Name>', methods=['POST'])
def create_instance(class_Name):
  try:
    data = request.json

    if not data:
      return jsonify({"error": "No data provided"}), 400
    
    interName = data['internName']
      
    # Si el procesamiento es exitoso, devuelve una respuesta JSON
    queryBoolean = PREFIXES + f"""
      ASK {{
        ?subclass rdfs:subClassOf* ont:{class_Name} .
        ?instanceIRI rdf:type ?subclass .
        FILTER(?instanceIRI = ont:{interName})
      }}
    """
    sparql.setQuery(queryBoolean)
    ret = sparql.queryAndConvert()
    if (ret['boolean'] == True):
      return jsonify({"error": "Instance already exists"}), 400
    
    label = data['label']
    stringQueryParts = [
      f"ont:{interName} rdf:type ont:{class_Name} .",
      f"ont:{interName} rdfs:label '{label}' ."
    ]

    dataProperties = data['dataProperties']
    if (len(dataProperties) > 0):
      for dp in dataProperties:
        if 'valueForm' in dp:
          stringQueryParts.append(f"ont:{interName} ont:{dp['IRI']} {dp['valueForm']} .")
        elif 'valuesFormArray' in dp:
          for value in dp['valuesFormArray']:
            if re.search(r'[0-9.]', value):
              stringQueryParts.append(f"ont:{interName} ont:{dp['IRI']} {value} .")
            elif type(value) == int:
              stringQueryParts.append(f"ont:{interName} ont:{dp['IRI']} '{value}' .")
    
    objectProperties = data['objectProperties']
    if (len(objectProperties) > 0):
      for op in objectProperties:
        for instance in op['instances']:
          stringQueryParts.append(f"ont:{interName} ont:{op['objectPropertyName']} ont:{instance} .")
    
    print(stringQueryParts)
    
    # TODO: hacer consulta final
    return jsonify({"message": "Instance created successfully"}), 201
  except ValueError as e:
    return jsonify({"error": str(e), "status": 400}), 400
      
  
if __name__ == "__main__":
  app.run(debug=True)