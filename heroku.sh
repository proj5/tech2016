pip install -r heroku_requirements.txt

python manage.py migrate

gunicorn --pythonpath app A2A.wsgi --log-file -
