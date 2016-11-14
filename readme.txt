# Bitcoin Output Watcher

Es una webapp que permite registrarse con un usuario, buscar outputs de transacciones en livenet y seguirlos. Cuando un output se consume se notifica a los seguidores vía email.

## Instalación

Crear una base de datos en postgres llamada outputwatcher.

Clonar el repositorio.

Crear un entorno virtual en ese direcitorio
```bashl
virtualenv env --distribute
```

Ingresar en el entorno, instalar las dependencias y migrar la base de datos.
```bashl
source dev/enter.sh
pip install -r requirements.txt
python manage.py migrate
```

Luego correr el servidor.
```bashl
python manage.py runserver
```

Instalar rabbitmq https://www.rabbitmq.com/download.html.

En otra terminal ingresar en el directorio del projecto, entrar en el entorno y ejecutar celery.
```bashl
source dev/enter.sh
celery -A outputwatcher worker -l info
```

Por último abrir un nueva terminal y ejecutar el script de python core/watcher.py que abrirá un websocket con BlockChain.

