web: gunicorn myapp.wsgi --log-file -
migrate: python manage.py migrate --settings=myapp.settings.production
seed: python manage.py loaddata myapp/item/fixtures/categories-data.json
seed: python manage.py loaddata myapp/item/fixtures/ingredients-data.json
seed: python manage.py loaddata myapp/item/fixtures/products-data.json