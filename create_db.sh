#!/bin/bash

rm -f mattlongweb/defaultdb
python manage.py syncdb --noinput --database=default
python manage.py migrate music --database=default

python manage.py createsuperuser
