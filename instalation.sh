python manage.py makemigrations
python manage.py migrate
python manage.py loaddata ./Tienda/fixtures/datos_prueba.json
python manage.py createsuperuser #username: grupo17, email: grupo17@gmail.com, password: 1234
python manage.py runserver