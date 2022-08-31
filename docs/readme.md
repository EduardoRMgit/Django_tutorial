# Documentación con Sphinx

## Requisitos Previos

* Crear un virtual environment fuera de la carpeta root del proyecto
```
python3 -m venv env
```

* Activar el virtual environment
```
source env/bin/activate
```

* Instalar base.txt (encontrada dentro del directorio cactus/requirements)
```
pip install -r base.txt
```

* Correr `cleanDataBase.sh` (dentro del directorio cactus/cactus)
```
./cleanDatabase.sh
```



## Para inicar sphinx en un proyecto nuevo

Crear una carpeta especial para correr el comando ```sphinx-quickstart```


### Instalación (solo si no se instaló base.txt previamente)

```
pip install -U sphinx
```

### Iniciar Sphinx

````
sphinx-quickstart
````

Seleccionar todos valores predeterminados

Ingresar el título del proyecto, autor y versión.

Se creará el archivo *conf.py*, *index.rst*, entre otros.

Dentro de *index.rst* se tienen que importar los demás archivos que se mostrarán en el home al dar la instrucción en la terminal `make html`

Dentro de `conf.py` se debe de ingresar la siguiente línea para configurar el path donde autodoc buscará los *docstrings*

```
import django

sys.path.insert(0, os.path.abspath('../cactus/'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'cactus.settings'
django.setup()
```

Así como la siguiente extensión:
```
extensions = [
    'sphinx.ext.autodoc',
    ....
]
```


## Estructura de documentación

Para trabajar sobre el proyecto Cactus tenemos el directorio docs.
Dentro de este se encuentra index.rst y los directorios explicación y sistemas.

Dentro de index se deben de importar los index respectivos de explicación y sistemas sin la extensión del archivo; es decir, sin `.rst` usando `/` como el indicador de directorio o archivo del que se tiene que importar.

### Ejemplo

Dentro de **index.rst**
`explicacion/explicacionIndex` Importaría el index dentro explicación

### Autodocumentación

Para autodocumentar a partir de los *docstrings* de los modelos, se debe de usar la *directiva*:

```
.. automodule:: app.models.nombredeModelo
  :members:
```

Automodule le índica a sphinx que debe de leer los docstrings. Lo siguiene es la ruta absoluta desde la carpeta cactus al archivo que se quiere autodocumentar.
Members indica que se quiere leer todo el contenido.


Para crear un archivo en donde ya se muestra contenido como en **texto.rst** dentro de la carpeta explicacion/directorio/texto.rst se debe debe de usar el formato rst que describo a continuación.


## Manera de documentar


```
Título
=======

.. image:: imagen.png

Texto Normal

*Texto con énfasis*

**Texto con énfasis fuerte**

`texto interpretado`

``inline literal``

- Elemento de lista no-ordenada
- Elemento de lista no-ordenada 2

1. Elemento de lista numerada y mostrado con énfasis
    #. sub elemento
    #. sub elemento
    #. sub elemento
2. Segundo elemento de lista numerada.
#. Elemento Auto enumerado.
```

## Docstrings

Para documentar un modelo se debe de iniciar el contenido con docstrings ` `` ` justo a por debajo de la clase o la función que se quiere documentar así como el siguiente ejemplo.
```
class UserProfile(models.Model):
    """aditional information for the user.

    ``Attributes:``

        - pk(int): Primary Key, one to one field to the django standard user \
            model

        - country: The country the user is from, ForeignKey(Country)

        - blocked_reason(char): Which is why the account was blocked

        - blocked_date(datetime): Date the account was locked

        - login_attempts(int): Number of login attempts

        - login_attempts(int): Number of login attemts to be blocked.

        - login_attempts_inside(int): Number of attemts inside to be blocked.

        - status(char): Status of the UserProfile
    """
    def reset_login_attempts(self):
        """
        **Description**
            This function set parameter of Account lockout to default values
        **Parameters**
            self
        """
        self.blocked_reason = self.NOT_BLOCKED
        self.blocked_date = None
        self.login_attempts = 0
        self.login_attempts_inside = 0
        self.save()
```

## Crear HTML, y PDF

Para ambos documentos es necesario posicionarse dentro de la carpeta docs.

### HTML
Para generar el HTML es necesario utilizar el comando `make html`. Con la configuración anterior, todo el proyecto ya debe estar listo para crear esta documentación.

### PDF
Para crear la documentación en PDF, es necesario instalar *latexmk* y *texlive-formats-extra* en la máquina en donde se esté trabajando con los siguientes comandos:

```
sudo apt install latexmk texlive-formats-extra
```
Posteriormente se puede correr el comando `make latex` seguido de `make latexpdf`
