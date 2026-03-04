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

* ahora configuramos los locales [Internationalization wagtail page](https://docs.wagtail.org/en/stable/advanced_topics/i18n.html#configuration) o ve directo a [configuración de locales](https://docs.wagtail.org/en/stable/advanced_topics/i18n.html#configuration) para más información. abre los settings base del proyecto y cambia o agrega a true estas variables.

```python
# config/settings/base.py
...
USE_I18N = True

WAGTAIL_I18N_ENABLED = True

USE_L10N = True # esta es opcional y es para formatear correctamente fechas y números
...
```

* agrega los lenguajes que quieres

```python
# config/settings/base.py
...
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('en', "English"),
    ('es', "Spanish"),
]
...
```

* vamos a agregar una configuración que dice el tutorial que lo hagamos pero es opcional para hacer la configuración en el admin (aunque lo vamos a sustituir por las dependencias de wagtail-localize)

```python
# config/settings/base.py
...
INSTALLED_APPS = [
    ...
    'wagtail.locales', # esto se va a cambiar, pero se deja para que tengas la referencia de que cambiar
    ...
]
...
```

* añadir un prefijo de lenguaje a las urls (basicamente para que las encuentres por "sitio.com/en/cv" para la versión inglés)

```python
# config/urls.py

...

from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    # aquí si te fijas falta search es porque se borró y se va agregar abajo
]

# hasta el final del archivo está el urlpatterns
# 
# urlpatterns = urlpatterns + [... 
# 
# pero  lo vamos a cambiar por esto:

urlpatterns += i18n_patterns(
    path('search/', search_views.search, name='search'), # y aquí está el search que borramos arriba
    path("", include(wagtail_urls)),
)
```

* configurar el lenguaje default (supongo que lo quieres en español)

```python
# config/settings/base.py
...
LANGUAGE_CODE = 'es'
...
```

* y en las urls poner esta configuración para que el lenguaje default no tenga el prefijo (prefix_default_language) y agregar un middleware.

```python
# config/urls.py
...
urlpatterns += i18n_patterns(
    path('search/', search_views.search, name='search'),
    path("", include(wagtail_urls)),
    prefix_default_language=False, #esto es lo que se agregó
)
...
```

```python
# config/settings/base.py
...
MIDDLEWARE = [
    ...
    'django.middleware.locale.LocaleMiddleware',
    ...
]
...
```

* opcional hay que agregar a las páginas un selector de idioma, pero este se agrega a los html, así que sólo dejo el snipet

```django
{% for language_code, language_name in LANGUAGES %}
    {% get_language_info for language_code as lang %}

    {% language language_code %}
        <a href="{% pageurl page.localized %}" rel="alternate" hreflang="{{ language_code }}">
            {{ lang.name_local }}
        </a>
    {% endlanguage %}
{% endfor %}
```

* instalar wagtail-localize [documentación de wagtail-localize](https://wagtail-localize.org/stable/)

```sh
pip install wagtail-localize==1.13 # la versión es opcional, pero la documentación que actualmente ves funciona con esta versión
```

* cambiar 'wagtail.locales' en INSTALLED_APPS

```python
# config/settings/base.py
INSTALLED_APPS = [
    ...
    "wagtail_localize",
    "wagtail_localize.locales",  # este reeemplaza "wagtail.locales"
    ...
```

* dice que hay que correr collect static, pero lo vamos a dejar casi para el final

* instalar wagtail-resume [página de github de wagtail resume](https://github.com/adinhodovic/wagtail-resume)

```sh
pip install wagtail-resume==2.12.0 # la versión es opcional, pero la documentación que actualmente ves funciona con esta versión
```

* configurar wagtail resume
```python
# config/settings/base.py
INSTALLED_APPS = [
    ...
    "wagtailmetadata",
    "wagtailmarkdown",
    "wagtail_resume",
    ...
]
```
```python
# config/urls.py
...
urlpatterns = [ # este es el primer urls patterns
    ...
    path("resume/", include("wagtail_resume.urls")), # hay que agregar este al final
]
...
```

* agregar el modelo a home/models.py para empezar a tener páginas de tipo resume o cv

```python
# home/models.py
...
from wagtail_resume.models import BaseResumePage

...

class ResumePage(BaseResumePage):
    pass
```

* correr makemigrations

```sh
python manage.py makemigrations
```

* aplicar migraciones

```sh
python manage.py migrate
```

* ahora si correr collectstatic

```sh
python manage.py collectstatic
```
