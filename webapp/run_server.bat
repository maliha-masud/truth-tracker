@echo off

rem Execute prestartup tasks
@REM python manage.py prestartup

rem Start the Django development server
python manage.py runserver
