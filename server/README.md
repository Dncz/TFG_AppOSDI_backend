Instalar pandas 3, además, habrá que instalar pyarrow
para iniciar el servidor de fuseki, ejecutar el siguiente comando:
```bash
java -jar fuseki-server.jar
```
Obviamente en el directorio donde se encuentre el archivo jar.

## Configuración


<!-- Consultas SPARQL -->
Esto devuelve todas las propiedades de la ontología y sus subpropiedades
```SQL
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ont: <http://www.ull.es/iis/simulation/ontologies/disease-simulation>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xml: <http://www.w3.org/XML/1998/namespace/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?dataTypeProperty ?subproperty
WHERE {
  {
    ?property rdf:type owl:DatatypeProperty .
  }
  UNION
  {
    ?property rdfs:subPropertyOf ?subproperty .
    ?subproperty rdf:type owl:DatatypeProperty .
  }
}

```	
Esto da las subpropiedades de las propiedades
```SQL
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ont: <http://www.ull.es/iis/simulation/ontologies/disease-simulation>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xml: <http://www.w3.org/XML/1998/namespace/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?dataTypeProperty ?subproperty
WHERE {
  {
    ?property rdf:type owl:DatatypeProperty .
  }
  UNION
  {
    ?subproperty rdfs:subPropertyOf ?property .
    ?subproperty rdf:type owl:DatatypeProperty .
  }
}

```	

Esto las propiedades que tienen subpropiedades
```SQL
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ont: <http://www.ull.es/iis/simulation/ontologies/disease-simulation>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xml: <http://www.w3.org/XML/1998/namespace/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?dataTypeProperty ?subproperty
WHERE {
  {
    ?property rdf:type owl:DatatypeProperty .
  }
  UNION
  {
    ?property rdfs:subPropertyOf ?subproperty .
    ?subproperty rdf:type owl:DatatypeProperty .
  }
}

```	