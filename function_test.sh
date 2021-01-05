rm db.sqlite3
python manage.py migrate --noinput
python test/functional/functional_test.py