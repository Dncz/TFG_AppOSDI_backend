# Trabajo Fin de Grado 
Grado en Ingeniería Informática - Universidad de La Laguna
# Interfaz para la interacción con una ontología de modelos de evaluación económica en salud
Interface for interaction with a health economic evaluation models ontology

## Introducción
La legislación española obliga a realizar un análisis exhaustivo de la viabilidad financiera, una evaluación económica, a todas las tecnologías sanitarias, técnicas o procedimientos que se quieran incluir al Servicio Nacional de Salud. Aunque una evaluación económica puede plantearse como parte de un ensayo clínico, hoy en día se emplean más los modelos de simulación debido a sus ventajas. Sin embargo, el uso de estos modelos enfrenta desafíos como la recopilación de datos de alta calidad, especialmente en el caso de enfermedades raras. Para abordar este problema, una de las soluciones posibles es el empleo de ontologías. Una ontología es una estructura semántica que organiza el conocimiento de un dominio específico de manera formal y explícita. 
En este contexto, el presente trabajo de fin de grado se basa en una línea de investigación en las que una investigación previa desarrolló una ontología, Standard Disease Ontology for Simulation (StaDiOS), la cual recopila información de estudios económicos-sanitarios sobre diversas enfermedades raras. Durante el desarrollo de este trabajo se emplea una versión avanzada de StaDiOS, denominada OSDI. Aunque existen herramientas para la inserción de información a la ontología, su complejidad dificulta su uso, especialmente para quienes no son expertos en dicha herramienta.
Para abordar este problema, el proyecto propone desarrollar una interfaz web que facilite la inserción de información en la ontología OSDI, denominada **AppOSDI**. Esta interfaz web permitirá a los usuarios consultar e insertar información a la ontología.

## Estructura del repositorio
El repositorio se divide en dos carpetas principales: `client`, `server` y `ontology`. La carpeta [client](https://github.com/Dncz/TFG_AppOSDI_frontend) contiene el código fuente del cliente de la aplicación web, mientras que la carpeta [server](https://github.com/Dncz/TFG_AppOSDI_backend) contiene el código fuente del servidor de la aplicación. La carpeta `ontology` contiene la ontología OSDI en formato .owl y .ttl.

## Autor
- Dana Belén Choque Zárate - alu0101328348@ull.edu.es