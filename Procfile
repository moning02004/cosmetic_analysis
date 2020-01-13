web: gunicorn myapp.wsgi --log-file -
migrate: python manage.py migrate --settings=myapp.settings.production
seed: python manage.py loaddata myapp/item/fixtures/ingredients_data.json myapp/item/fixtures/categories_data.json myapp/item/fixtures/products_data.json
