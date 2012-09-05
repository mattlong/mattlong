#!/bin/bash

DEBUG=$1

if [ "$DEBUG" == "true" ]; then
    initdata=""
else
    initdata="--no-initial-data"
fi

rm -f mattlongweb/defaultdb

python manage.py syncdb --noinput --database=default

python manage.py migrate base --database=default $initdata
python manage.py migrate blog --database=default $initdata
python manage.py migrate music --database=default $initdata
python manage.py migrate bookmarks --database=default $initdata

#python manage.py createsuperuser
