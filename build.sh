#!/bin/bash

perl -e 'print scalar(localtime) . "\n"'

python manage.py reset core --noinput
python manage.py syncdb
cd data/manuscripts
python import.py
python merge.py

perl -e 'print scalar(localtime) . "\n"'