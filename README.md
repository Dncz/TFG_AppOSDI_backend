# Trabajo Fin de Grado 
Grado en Ingeniería Informática - Universidad de La Laguna
# Interfaz para la interacción con una ontología de modelos de evaluación económica en salud
Interface for interaction with a health economic evaluation models ontology

## Resumen
La legislación española obliga a realizar un análisis exhaustivo de la viabilidad financiera, una evaluación económica, a todas las tecnologías sanitarias, técnicas o procedimientos que se quieran incluir al Servicio Nacional de Salud. Aunque una evaluación económica puede plantearse como parte de un ensayo clínico, hoy en día se emplean más los modelos de simulación debido a sus ventajas. Sin embargo, el uso de estos modelos enfrenta desafíos como la recopilación de datos de alta calidad, especialmente en el caso de enfermedades raras. Para abordar este problema, una de las soluciones posibles es el empleo de ontologías. Una ontología es una estructura semántica que organiza el conocimiento de un dominio específico de manera formal y explícita.
Este trabajo de fin de grado se basa en una línea de investigación en el que un trabajo previo desarrolló una ontología, la cual recopila información de estudios económicos-sanitarios sobre diversas enfermedades. Durante el desarrollo de este trabajo se emplea una versión avanzada de dicha ontología combinada con otras ideas, denominada OSDI. Aunque existen herramientas para la inserción de información a la ontología, su complejidad dificulta su uso, especialmente para quienes no son expertos en dicha herramienta.
Para abordar este problema, el proyecto propone desarrollar una interfaz web que facilite la inserción de información en cualquier ontología. En este caso, se ha desarrollado una aplicación denominada CRUDOnt.
Esta aplicación, CRUDOnt, permitirá a los usuarios consultar e insertar información a la ontología.

## Abstract
Spanish legislation requires a full financial feasibility analysis, an economic evaluation, for all health technologies, techniques, or procedures to be included in the National Health Service. Although an economic evaluation can be part of a clinical trial, simulation models are nowadays more widely used due to their advantages. However, the use of these models presents challenges such as the collection of high-quality data, especially in the case of rare diseases. To address this problem, one of the possible solutions is the use of ontologies. An ontology is a semantic structure that organises domain-specific knowledge in a formal and explicit way. 
In this bachelor thesis follows a line of research in which previous work developed an ontology, which collects information from health-economic studies on various diseases. During the development of this work, an advanced version of this ontology combined with other ideas, called OSDI, is used. Although there are tools for inserting information into the ontology, its complexity makes it difficult to use, especially for non-experts.
To solve this problem, the project proposes to develop a web interface that facilitates the insertion of information into any ontology. In this case, an application called CRUDOnt has been developed.
This application, CRUDOnt, will allow users to query and insert information into the ontology.



## Estructura del repositorio
El repositorio se divide en dos carpetas principales: `client`, `server` y `ontology`. La carpeta [client](https://github.com/Dncz/TFG_CRUDOnt_frontend) contiene el código fuente del cliente de la aplicación web, mientras que la carpeta [server](https://github.com/Dncz/TFG_CRUDOnt_backend) contiene el código fuente del servidor de la aplicación. La carpeta `ontology` contiene la ontología OSDI en formato .owl y .ttl.

## Autor
- Dana Belén Choque Zárate - alu0101328348@ull.edu.es