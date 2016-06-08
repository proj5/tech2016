#!/bin/sh

# Clear old database
rm db.sqlite3

# Create new database
python manage.py migrate

# Install fixture

# username:password
# admin:admin123
# user:user1234
python manage.py loaddata auth.json
python manage.py loaddata users.json
python manage.py loaddata topics.json
python manage.py loaddata posts.json
python manage.py loaddata questions.json
python manage.py loaddata comments.json
python manage.py loaddata notifications.json

# Force check pep8 when commit
commit_script="#!/bin/bash
set -e
echo '---------------------------------'
pep8 --exclude=*/migrations/,env,A2A .
echo '---------------------------------'
python manage.py test
"

echo "$commit_script" > .git/hooks/pre-commit
chmod 755 .git/hooks/pre-commit