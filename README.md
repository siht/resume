# resume
proyecto de wagtail preparado para empezar sitios con páginas traducidas para hacer cv

## dependencias para iniciar desde 0

* python 3.14.*
* wagtail 7.3rc1

### como instalar desde 0 por cualquier problema

* crea un entorno virtual

* instala wagtail [wagtail getting started page](https://docs.wagtail.org/en/stable/getting_started/tutorial.html) para más detalles

```sh
pip install wagtail==7.3rc1 # o solo wagtail pero si hay incompatibilidades vas a tener que hacerlo con la nueva documentación
```

* inicia el proyecto, yo te recomiendo que lo generes así:

```sh
wagtail start config resume # así te creará una carpeta llamada resume y la configuración la pondrá en una carpeta llamada config como la estructura de este proyecto
```

* instala las dependencias del proyecto, que están dentro de la carpeta resume

```sh
cd resume
pip install -r requirements.txt
```
