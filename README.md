# Cactus
[![Build Status](https://travis-ci.com/brattdev/Cactus.svg?token=UzKcpqNqhEMe6rucMNj8&branch=master)](https://travis-ci.com/brattdev/Cactus)

[Kubernetes](#Kubernetes)

[APIdocs](#apidocs)

## Tutorials
[K8 Local to Prod](https://medium.com/@markgituma/kubernetes-local-to-production-with-django-2-docker-and-minikube-ba843d858817)
[Short minikue django](https://github.com/nhatthai/django-minikube)

<a name="Kubernetes"></a>
## Kubernetes

Kubernetes es una plataforma para correr un servicio a lo largo de muchos
computadoras o VirtualMachines. Esto lo hace a través de algo llamado deployments.
Los deployments corren pods, los cuales siempre están dentro de una misma maquina.
Además, dentro tienen contienen contenedores, hechos normalmente con Docker.
La idea es que los contenedores tengan microaplicaciones, que se corren on-demand.
Esto debido a que los contenedores pueden compartir un sistema operativo,
pero pueden correr como maquinas separadas a las cuales se les asigna sus
propios recursos.
Los deployments obtienen información de cuantos pods correr,
se puede actualizar un pod esperando a que los otros dejen de ser
usados y así se mantiene un continuous deployment o CD.

Lo interesante de kuberentes es que tiene un mecanismo para siempre mantener a
los pods vivos cada vez que pase algo malo (failover),
escalar los recursos y actualizar la aplicación.

### Instalar

[Docker](https://docs.docker.com/install/) para crear los contenedores
[Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) Para darle
ordenes al k8 (kubernetes) cluster, desde tu compu.
In Linux, download the latest executable with:
```
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
```

Make the kubectl binary executable.

`chmod +x ./kubectl`

Move the binary in to your PATH.

`sudo mv ./kubectl /usr/local/bin/kubectl`

Test to ensure the version you installed is up-to-date:

`kubectl version`


[VirtualBox](https://www.virtualbox.org/wiki/Downloads) para que minikube se cree
en un VM.

[Minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/)
En Linux:
`curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && chmod +x minikube`
Y para añadirlo a path:
`sudo install minikube /usr/local/bin`


### Correr django localmente
Para hacer un deploy de Cactus debes tener un app de django
 en un carpeta por ej. `cactus`

Primero tienes que conectarte a un servidor donde harás deploy a tus pods,
en este caso usaremos minikube que es una maquina virtual en tu lap que
tiene kubernetes instalado.

`minikube start`

Corriendo `minikube dashboard &` puedes mantener un dashboard abierto, donde
puedes ver el estado de tus deployments, services, pods, etc.

Luego modificas bash para correr dentro de minikube, osea en docker daemon de
minikube, para que puedas jalar las imágenes directo y no las tengas que poner
en un docker registry.

`eval $(minikube docker-env)`

Primero haces una imagen en la carpeta `/builder` con el paquete django
ya instalado para que cualquier cambio lo podamos hacer sobre una imagen encima.
La llamamos `brattdev/python3.7_django`. Esto con un `Dockerfile` que debe de
estar en la carpeta `builder`

El comando en general es:
`docker build --rm -f <Dockerfile> -t <IMAGE_NAME>:<TAG> .`

Donde <IMAGE_NAME> es el nombre de la imagen y <TAG> es la version. el punto
indica el path desde donde lo armas osea "." es donde estas. El `--rm` es para
que se borren las imágenes con el mismo nombre.

En este caso:

`docker build --rm -f Dockerfile_builder -t brattdev/python3.7_django .`

Seguidamente, armas la imagen de la app de django que debe de estar al lado de manage.py

`docker build --rm -t netopaas/brattdev:cactus0.1 .`

Puedes correr el cluster con su deployment, servicio e ingress de una corriendo:

`kubectl apply -f cluster/`

y quitarlo todo con

`kubectl delete -f cluster/`

Para poder acceder a la app desde una lan, debes de añadirle un bridge desde
networking en la configuración de la VM. Anotas el mac de la VM y puedes usar

`arp -a`

Para buscar la MAC y obtener el IP address. Después de eso ya deberías de poder
meterte desde cualquier compu en la LAN. En la dirección:

`<ip>:30000/admin`

Solo que el IP debe de estar en tus `ALLOWED_HOSTS` de la app de django.
Esto cambiará cuando ya esté en la nube.

### Subir la web de sphinxdoc

Solo debes de armar la imagen después de haber armado las otras docs

`docker build -t netopaas/brattdev:sphinxdoc -f Dockerfile_sphinx .`

Y usar los manifest en la carpeta `cluster_sphinx` para k8

`kubectl apply -f cluster_sphinx`


### Detalle de servicos de Kubernetes

Los diferentes servicios están separados en archivos. El `deployment.yaml` es el que crea y cuida los pods.
El `service.yaml` es el que permite a los pods hablar entre ellos. O a una base de datos con unos pods.
El `ingress.yaml` es un reverse proxy y puede ser usado para asignar un host o dirección
a un servicio en específico.

El nombre del host desde donde acceder a la app es cactus.com, como fue
escrito en `ingress.yaml`. El host (eg. cactus.com), debe de estar en ls
ALLOWED_HOSTS" de django tmb debes de activar el addon de nginx

`minikube addons enable ingress`

### Troubleshooting
Esta cheatsheet ayuda mucho: https://kubernetes.io/docs/reference/kubectl/cheatsheet/#kubectl-context-and-configuration
Si el deployment no encuentra las imágenes no te jalan con esto,
puede ser que no estés dentro del docker daemon. Las imágenes que creaste
dentro del docker daemon de minikube se
quedan ahí, así que te debes de meter así `eval $(minikube docker-env)`
para poder acceder. Además, puedes correr esto:

`kubectl config use-context minikube`

Para ver si hay un error en los containers y porque, primero obtén el nombre del pod:

`kubectl get pod`

y luego saca su log con:

 `kubectl --v=8 logs <nombre-pod>`

Además, puedes correr comandos dentro de la imagen para ver que puede estar mal,
pero ten cuidado que en realidad estas haciendo un container temporal, no
harás cambios a la imagen en general.

`docker run --rm -it netopaas/brattdev:cactus0.1 sh`

Y si no quieres que se corra el server, overrideas el entrypoint de esta manera:

`docker run --rm -it --entrypoint "sh" netopaas/brattdev:cactus0.1`

Y si quieres acceder al pod ya en el cluster:

`kubectl exec -it cactus-site-c8dd466bd-7lf88 -- /bin/bash`

Te puede servir este comando que accede al primer pod en la lista de pods,
 cuyo label sea app:web:

`kubectl exec -it $(kubectl get pod -l app=web -o jsonpath="{.items[0].metadata.name}") -- /bin/bash`

Borrar las imagenes sin nombre:
`docker rmi $(docker images -f dangling=true -q)`

Meterte a la base de datos postgresql del deployment de postgres
`kubectl exec -it $(kubectl get pod -l app=postgres-container -o jsonpath="{.items[0].metadata.name}") -- /bin/bash`

`psql -U admin -d postgres`

=======

<a name="apidocs"></a>
# Intstrucciones para APIdocs

## Docs

[http://apidocjs.com/](http://apidocjs.com/)

## Instalación

`npm install apidoc -g`

## Uso
El código para generar los apidocs de banca sería (estando en el root del proyecto):

 `apidoc -i cactus/ -o apiDocs/`

Para crear la documentación en la carpeta `apidoc` de todos los archivos de código (c++, c#, ruby, perl, python) en la carpeta `myapp` usando el template `mytemplate` usas:

`apidoc -i myapp/ -o apidoc/ -t mytemplate/`

Si omites el `-t` se usará un template default.

### Inicialización

Ahora `apidoc.json`. En este archivo se pone la información general de la doc. Su formato es este:

```
{
  "name": "example",
  "version": "0.1.0",
  "description": "apiDoc basic example",
  "title": "Custom apiDoc browser title",
  "url" : "https://api.github.com/v1",
  "header": {
    "title": "My own header title",
    "filename": "header.md"
  },
  "footer": {
    "title": "My own footer title",
    "filename": "footer.md"
  }
}
```

La tabla al final explica los campos

## Concepto

**Apidocs** se usa para documentar **RESTful APIs**, a través de comentarios en el código. Éstas son funciones que usarán clientes (**API**) a través de la web, en específico el protocolo *http*. La parte de **REST** se debe a la convención que se usa para hacer llamadas, como las son el típico **POST** y **GET** (u otras como **PATCH**).

Éstas funciones tienen un formato en específico. Todas tiene un tipo de request (como **POST**), un *path*, osea la *url* por medio de la cual es llamada la función y permisos. Es por esto que la documentación tiene una medallita para el tipo de request, un botón de info para los permisos y hasta ejemplos de *request* a la función.
Además, puedes tener seguimiento de versiones.

 Todo esto se puede ver en la siguiente imágen:

 ![alt text](/misc/fields.png "Los campos")

 ![alt text](/misc/requests.png "Los requests")

En el caso de **Django**, se usa este tipo de documentación para las funciones de las **Views**. Que son las que están haciendo requests a las bases de datos o modelos con las que se trabajan, entre otras cosas.

### Comentarios

Solo se creará algo si tienes comentarios en tu código. Los puedes poner en cualquier parte, pero de preferencia ponlos dentro de la función. Los cuales tienen la siguiente forma:
```
"""
 @api {get} /user/:id Request User information
  @apiName GetUser
 @apiGroup User

 @apiParam {Number} id Users unique ID.

 @apiSuccess {String} firstname Firstname of the User.
 @apiSuccess {String} lastname  Lastname of the User.

 @apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     {
       "firstname": "John",
       "lastname": "Doe"
     }

 @apiError UserNotFound The id of the User was not found.

 @apiErrorExample Error-Response:
     HTTP/1.1 404 Not Found
     {
       "error": "UserNotFound"
     }
"""
```
* El `@api` es necesario, no se hará una entrada si no lo pones.
  * `get` es el tipo de request como **POST**.
  * `/user/:id` es la url desde la que
se hace la request.
 * Y luego sigue una descripción de lo que hace la función.
* El `@apiName` es el nombre de la función.
* El `@apiGroup` es para agrupar funciones bajo un header en las docs
* El `@apiParam` da el type del parámetro, su nombre y una descripción
* El `@apiSuccess` da el type de las variables de retorno, su nombre y una descripción.

Con los demás dejas ejemplos de como se ve un succes o un error y con `@apiError` el tipo de error que se regresa y una descripción.


### Tips
Puedes usar `@apiDefine [nombre bloque]` para crear un bloque que quieras reusar y `@apiuse [nombre bloque]` para llamarlo. L cual te puede ahorrar mucho tiempo.

Otra buena práctica es poner las docs de viejas versiónes o bloque que reutilizaras mucho en archivo llamado `_apidocs.py` para acceder a ellos de otras partes y que no hagan mucho ruido.


### Tablita

<table>
      <thead>
      <tr>
        <th>Name</th>
        <th>Description</th>
      </tr>
      </thead>
      <tbody>
      <tr>
        <td class="code">name</td>
        <td>Name of your project.<br>If no <code>apidoc.json</code> with the field exists, then apiDoc try to determine the the value from <code>package.json</code>.</td>
      </tr>
      <tr>
        <td class="code">version</td>
        <td>Version of your project.<br>If no <code>apidoc.json</code> with the field exists, then apiDoc try to determine the the value from <code>package.json</code>.</td>
      </tr>
      <tr>
        <td class="code">description</td>
        <td>Introduction of your project.<br>If no <code>apidoc.json</code> with the field exists, then apiDoc try to determine the the value from <code>package.json</code>.</td>
      </tr>
      <tr>
        <td class="code">title</td>
        <td>Browser title text.</td>
      </tr>
      <tr>
        <td class="code">url</td>
        <td>Prefix for api path (endpoints), e.g. <code>https://api.github.com/v1</code></td>
      </tr>
      <tr>
        <td class="code" id="configuration-settings-sample-url">sampleUrl</td>
        <td>If set, a form to test an api method (send a request) will be visible. See <a href="#param-api-sample-request">@apiSampleRequest</a> for more details.</td>
      </tr>
      <tr>
        <td class="code" colspan="2">header</td>
      </tr>
      <tr>
        <td class="code">&nbsp;&nbsp;&nbsp;&nbsp;title</td>
        <td>Navigation text for the included header.md file.<br>(watch <a href="#headerfooter">Header / Footer</a>)</td>
      </tr>
      <tr>
        <td class="code">&nbsp;&nbsp;&nbsp;&nbsp;filename</td>
        <td>Filename (markdown-file) for the included header.md file.</td>
      </tr>
      <tr>
        <td class="code" colspan="2">footer</td>
      </tr>
      <tr>
        <td class="code">&nbsp;&nbsp;&nbsp;&nbsp;title</td>
        <td>Navigation text for the included footer.md file.</td>
      </tr>
      <tr>
        <td class="code">&nbsp;&nbsp;&nbsp;&nbsp;filename</td>
        <td>Filename (markdown-file) for the included footer.md file.</td>
      </tr>
        </td>
      </tr>
      </tbody>
    </table>
