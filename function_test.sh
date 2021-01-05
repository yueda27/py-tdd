rm db.sqlite3
pipenv run python manage.py migrate --noinput
pipenv run python test/functional/functional_test.py