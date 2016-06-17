@echo off
:: !Clear old database
set name=db.sqlite3

set argc=0
for %%x in (%*) do Set /A argc+=1
if %argc% GEQ 1 set name=dbtest.sqlite3

echo %name%
del %name%

:: !Create new database
python manage.py migrate

:: Install fixture

:: username:password
:: admin:admin123
:: user:user1234
:: quang:admin123
python manage.py loaddata auth.json 
python manage.py loaddata users.json
python manage.py loaddata topics.json
python manage.py loaddata posts.json
python manage.py loaddata questions.json
python manage.py loaddata comments.json
python manage.py loaddata notifications.json

:: Force check pep8 when commit
set filename=.git/hooks/pre-commit
echo #!/bin/bash >%filename%
echo set -e >>%filename%
echo echo '---------------------------------' >>%filename%
echo pep8 --exclude=*/migrations/,env,A2A . >>%filename%
echo echo '---------------------------------' >>%filename%
echo python manage.py test >>%filename%
