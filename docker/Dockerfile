# Usamos una imagen con django para no tener que volver a cargar todo cuando
# queramos hacer cambios al Dockerfile
FROM 906062568112.dkr.ecr.us-east-2.amazonaws.com/cactus:django3.7 AS whole_app
LABEL maintainer="netopaas@gmail.com"

WORKDIR /cactus


COPY docker/entrypoint.sh entrypoint.sh

#Un RUN corre un comando y crea una nueva capa sobre la imagen
RUN ["chmod", "+x", "entrypoint.sh"]
COPY known_hosts /root/.ssh/known_hosts

#Nos dice el comando que se correrá cuando corramos la imagen
# a diferencia de CMD, que pone un comando estándar cuando no damos
# ningún argumento
# entrypoint siempre se corre al correr la imagen
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]

COPY /cactus/. .
