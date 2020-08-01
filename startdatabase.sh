python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata db.json -e contenttypes -e auth -e sessions -e admin
