FROM python:3.9-alpine3.13
LABEL maintainer="matiaszazzali"

# recomendado para usar python. Unbuffered para evitar demoras en ver los outputs de python
ENV PYTHONUNBUFFERED 1

# copio carpetas locales a la imagen de docker, seteo el workdir y expongo el puerto de la imagen
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt 
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# ARG DEV=false por defecto no corro en modo de desarrollo. si lo corro a traves de docker compose, lo cambia a True
# uso un solo RUN porque de usar uno para cada linea, se crea una capa de la imagen nueva para cada una y aumenta el peso
# primero creo un virtual env. Hay controversia, muchos dicen que en docker no deberia crear virtual env, pero me salva de incompatibilides en las dependencias de la imagen de python de base que uso
# remove tmp directory, no quiero dependencias extras una vez que se crearon. borro los files para dejar siempre la imagen de docker lo mas ligera posible
# adduser crea un nuevo usuario en la imagen. es buena practica NO usar el root user. si se corre la app con root user, un atacante tendria permisos completos
# luego explicito el nombre del usuario "django-user", lo elijo yo
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# actualizo el env de la imagen, particularmente la variable de entorno PATH. 
# es la variable que se crea por defecto en linux, define todos los directorios donde se pueden correr ejecutables
ENV PATH="/py/bin:$PATH"

# el USER debe ser la ultima linea del dockerfile. cambia el usuario.
USER django-user
