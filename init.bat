@echo off
:: !Clear old database
del db.sqlite3

:: !Create new database
python manage.py migrate

:: Install fixture

:: username:password
:: admin:admin123
:: user:user1234
python manage.py loaddata auth.json
python manage.py loaddata users.json
python manage.py loaddata topics.json
python manage.py loaddata questions.json
python manage.py loaddata answers.json
python manage.py loaddata comments.json

:: Force check pep8 when commit
set filename=.git/hooks/pre-commit
echo #!/bin/bash >%filename%
echo set -e >>%filename%
echo echo '---------------------------------' >>%filename%
echo pep8 --exclude=*/migrations/,env,A2A . >>%filename%
echo echo '---------------------------------' >>%filename%
echo python manage.py test >>%filename%
