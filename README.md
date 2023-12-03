# Contenedor Docker Python


## 1. Instalación

Para descargar la aplicación del repo, se debe escribir el siguiente comando:

```
$ git clone https://github.com/FragmentosTemporales/flask-REST-API-Postgresql.git
```


### Instalación de Docker Compose

Para instalar la aplicación debes ejecutar el siguiente código:

```
null
```


### Variables de entorno

Al interior de la carpeta /Sripts debes crear un documento env.env el cual debe contener las siguiente variables, puedes guiarte con el documento example.env :

```
FLASK_ENV=dev

JWT_SECRET_KEY=
JWT_ACCESS_TOKEN_EXPIRES_HOURS=
JWT_ACCESS_TOKEN_EXPIRES_DAYS=
RECORDS_PER_PAGE=
SECRET_KEY=

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=
```


## 2. Ejecución

Para ejecutar la aplicación debes ingresar el siguiente comando:

```
python manage.py run
```

Para ejecutar los test unitarios y flake8

```
python manage.py test && flake8
```


## 3.- ¿Qué estamos ejecutando?

Al ejecutar el manage.py estamos creando una Rest API Flask, la cual se conecta a una base de datos POSTGRESQL.
Esta base de datos cuenta con endpoints aplicando un CRUD a un modelo de Usuario. 


## 4.- Bibliografía

```
null
```