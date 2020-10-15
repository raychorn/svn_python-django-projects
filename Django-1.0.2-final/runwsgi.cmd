@echo off
set PYTHONPATH=c:\python25;Z:\python projects\_django_0_96_2;Z:\python projects\@lib
python manage.py runwsgi --host 127.0.0.1 --port 8888
