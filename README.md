# resume
proyecto de wagtail preparado para empezar sitios con páginas traducidas para hacer cv

## dependencias (probadas, cualquier cambio va por tu cuenta)

* python 3.14.*
* wagtail 7.3rc1

## links útiles para que no busques por todo el texto

* [wagtail getting started page](https://docs.wagtail.org/en/stable/getting_started/tutorial.html)
* [Internationalization wagtail page](https://docs.wagtail.org/en/stable/advanced_topics/i18n.html#configuration)
* [configuración de locales](https://docs.wagtail.org/en/stable/advanced_topics/i18n.html#configuration)
* [documentación de wagtail-localize](https://wagtail-localize.org/stable/)
* [página de github de wagtail resume](https://github.com/adinhodovic/wagtail-resume)


## inicio rápido

* descarga este repositorio

* crea un entorno virtual

* entra a resume e instala las dependencias

```sh
pip install -r requirements.txt
```

* aplicar migraciones

```sh
python manage.py migrate
```

* instalar configuración previa, esto nos da un usuario (yo), pass (yo), que ya tiene configurada la mayor parte de lo que explico casi al final de [como instalar desde 0 por cualquier problema](#como-instalar-desde-0-por-cualquier-problema) 

```sh
python manage.py loaddata data.json
```

* recolectar estáticos

```sh
python manage.py collectstatic
```

* opcional pero muy deseable (casi obligatorio para que tengas todas las traducciones), instalar gettext para correr, te dejo este extracto, pero casi al final de estas instrucciones puedes ver para otros sistemas.

```sh
# así lo instalas en linux/wsl
sudo apt update && sudo apt install gettext
```


```sh
django-admin compilemessages
```

* iniciar el servidor (asegurate de no cambiar el puerto a otro que no sea el 8000)

```sh
python manage.py runserver
```

## como instalar desde 0 por cualquier problema

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

* por alguna razón algunas traducciones se quedaron en los archivos, así que toca hacer los pasos de configurar las traducciones de django y crear una carpeta llamada locale en la raíz del proyecto

```python
# config/settings/base.py
LOCALE_PATHS = [
    BASE_DIR/'locale',
]
```

```sh
# ve a la raíz del proyecto, no del repositorio y ejecuta para que coincida con la configuración que acabamos de poner
mkdir locale
```

* si no lo tienes instalado hay que instalar gettext (esto se probó en wsl)

```sh
# ubuntu / wsl
sudo apt update && sudo apt install gettext
```

```sh
# macos
brew install gettext
brew link --force gettext
```

```sh
# en windows con chocolatey o ve a la página de gnu gettext for windows (https://mlocati.github.io/articles/gettext-iconv-windows.html)
choco install gettext
```

* después de instalar gettext hay recolectar los mensajes y compilarlos, pero antes hay que copiar el html que no está completamente configurado para ser traducido por wagtail-localize

```sh
# home/templates/
mkdir wagtail_resume
# una vez creado el directorio dentro vas a crear el siguiente archivo con este nombre resume_page_body.html
```

```django
{% comment %}
es el direcotrio home de tu proyecto, no de tu máquina
home/templates/wagtail_resume/resume_page_body.html
te dejo el archivo completo para que no batalles buscando que poner
{% endcomment %}
{% load i18n %}
{% load static %}
{% load wagtailimages_tags %}
{% load wagtailmarkdown %}
{% load wagtail_resume_extras %}

{% if debug_i18n %}
  {% include 'wagtail_resume/localization_dropdown.html' %}
{% endif %}
{# djlint:off #}
<!-- We set bg_color within a style tag to only apply bg_color when having a min-width. Weasyprint does not support @media queries
     therefore setting a min-width to 1px ensures that the bg_color does not get applied when generating pdfs. -->
{% with page.background_color|default_if_none:"#343A40" as bg_color %}
<style>
  @media (min-width: 1px) {
    .container {
      background-color: {{ bg_color }};
    }
  }

  @page {
    margin: 0.75in 0.75in 0.85in 0.75in;
    size: Letter;

    @bottom-center {
      content: "{% trans "Page" %} " counter(page) " {% trans "of" %} " counter(pages);
      font-size: 8pt;
      color: #666666;
      font-style: italic;
      font-family: "Roboto", "Noto Sans";
    }
  }
</style>
{% endwith %}
<body style="font-family: {% if page.font %}'{{ page.font|title }}', {% endif %}'Roboto', 'Noto Sans'">
{# djlint:on #}
<div class="container">
  <div class="resume">
    <div class="personal-info">
      <div>
        <h2 class="mt-2 mb-0">{{ page.full_name }}</h2>
        {% if page.role %}<h2 class="mt-2">{{ page.role }}</h2>{% endif %}
        <div class="social-links">
          {% for social_link in page.social_links %}
            <div class="social-links">
              <a class="social-link" href="{{ social_link.value.url }}">
                {% if social_link.value.logo %}
                  {% image social_link.value.logo original class="mt-1" %}
                  <span class="ml-1">{{ social_link.value.text }}</span>
                {% else %}
                  <span class="ml-0">{{ social_link.value.text }}</span>
                {% endif %}
              </a>
            </div>
          {% endfor %}
        </div>
        {% if page.display_last_update %}
          <p class="small italic mt-1">{% trans "Last update" %}: {{ page.latest_revision_created_at|date }}</p>
        {% endif %}
      </div>
      <div class="mt-4">{% image page.photo original class="photo" %}</div>
    </div>
    <div>
      <h2 class="mt-4 mb-0">
        {% if page.about_icon %}<i class="{{ page.about_icon }}"></i>{% endif %}
        <span>{% trans "About" %}</span>
      </h2>
      <hr />
      <p>{{ page.about | markdown }}</p>
    </div>
    {% for block in page.resume %}{{ block }}{% endfor %}
    {% if page.pdf_generation_visibility == "always" or user.is_authenticated and page.pdf_generation_visibility == "authenticated" %}
      <div class="pdf-buttons">
        <a class="pdf"
           href="{% url 'generate_resume_pdf' %}?page_id={{ page.id }}"
           title="Download standard resume PDF">{% trans "Get PDF" %}</a>
        <a class="pdf pdf-academic"
           href="{% url 'generate_academic_resume_pdf' %}?page_id={{ page.id }}"
           title="Download academic-style resume (professional CV format)">{% trans "Get Academic PDF" %}</a>
      </div>
    {% endif %}
  </div>
</div>
</body>
```

```sh
# crear archivo .po (necesario gettext)
django-admin makemessages -l es -e html
```

* escribes las traducciones que te pide, se va a generar un árbol de directorios con un archivo (locale/es/LC_MESSAGES/django.po) con placeholders para que coloques las traducciones, en mi caso usé sólo español y una vez que termines ahora hay que compilarlo

```sh
django-admin compilemessages
```

* ahora si correr collectstatic

```sh
python manage.py collectstatic
```

* generar un superusuario

```sh
python manage.py createsuperuser
```

* iniciar el servidor

```sh
python manage.py runserver
```

* dentro del admin, debes de dar de alta un nuevo locale, con la configuración de este README el default es español, así que propiedades/regiones das de alta en inglés en la parte de "Add a locale", ahí te dará el idioma inglés, lo único que debes hacer es en la parte de "Sincronizar contentido desde otra región" seleccionar spanish y guardar.

* dentro del admin, también debes cambiar el puerto de sitios por el que estás usando, así que ve a propiedades/sitios y a localhost le cambias el puerto en mi caso será 8000 y guardas