python3 manage.py makemigrations
python3 manage.py migrate
if [ ! -f "/__dbloaded__" ] 
then
    echo "LOADING INITIAL DATA from data.json into database"
    python3 manage.py loaddata data.json -e contenttypes -e auth -e sessions -e admin
    touch "/__dbloaded__"
fi
# python3 manage.py loaddata db_int.json -e contenttypes -e auth -e sessions -e admin
# python3 manage.py loaddata data.json -e contenttypes -e auth -e sessions -e admin
# python3 manage.py loaddata db.json -e contenttypes -e auth -e sessions -e admin
