python manage.py makemigrations
python manage.py migrate
python manage.py loaddata ./Tienda/fixtures/datos_prueba.json
python manage.py createsuperuser #username: admin, email: admin@admin.com, password: admin
python manage.py runserver