#!/bin/bash

rm -f mattlongweb/defaultdb

python manage.py syncdb --noinput --database=default

python manage.py migrate base --database=default
python manage.py migrate blog --database=default
python manage.py migrate music --database=default
python manage.py migrate bookmarks --database=default

#python manage.py createsuperuser
