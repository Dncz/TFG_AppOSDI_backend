
# CRUDOnt server
Este repositorio contiene el servidor para la aplicación web CRUDOnt, una interfaz que facilita la inserción y consulta de información en cualquier ontología.

## Requisitos Previos
Antes de instalar y ejecutar el servidor, asegúrate de tener instalados los siguientes componentes:
- Python (versión 3.8 o superior)
- pip (versión 21 o superior)
- SPARQLWrapper (versión 2.0.0)
- Flask (versión 3.0.2)
- flask-cors (versión 4.0.0 o superior)

## Instalación
Sigue los pasos a continuación para instalar y configurar el servidor de CRUDOnt:
1. **Clona el repositorio:**
  ```bash
  git clone https://github.com/Dncz/TFG_CRUDOnt_backend.git
  cd TFG_CRUDOnt_server
  ```

2. **Descargar Fuseki:**
  Descarga el archivo `apache-jena-fuseki-4.4.1.zip` desde la página oficial de [Apache Jena](https://jena.apache.org/documentation/fuseki2/#download-fuseki-with-ui) y descomprímelo en el directorio raíz del proyecto o en cualquier otro directorio de tu elección.
  Inicia el servidor (dentro de la carpeta descomprimida) de Fuseki ejecutando el siguiente comando:
  ```bash
  java -jar fuseki-server.jar
  ```
  Asegúrate de que el servidor de Fuseki esté en ejecución antes de iniciar el servidor de la aplicación.

  Crear un dataset en Fuseki llamado `osdi` y cargar la ontología `osdi.owl` en el dataset creado.
  Nota: La ontología `osdi.owl` se encuentra en la carpeta `ontologies`. Debes cambiar el formato .owl a .ttl para poder cargarla en Fuseki.
  

## Ejecución
Primero asegúrate de que el servidor de la aplicación y Fuseki estén en ejecución antes de iniciar el servidor. Para iniciar el servidor, ejecuta el siguiente comando:
```bash
python3 app.py
```
Al ejecutar el comando anterior, el servidor se iniciará en el puerto 5000. Para acceder a la aplicación, abre un navegador web y navega a la dirección `http://localhost:5000/`.


## Licencia
Este proyecto está licenciado bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para obtener más información.

## Contacto
Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto conmigo a través de mi dirección de correo electrónico:
alu0101328348@ull.edu.es