SHELL := /bin/bash

manage_py := python app/manage.py

migrate:
	$(manage_py) migrate

shell:
	$(manage_py) shell_plus --print-sql

run:
	$(manage_py) runserver

worker:
	cd app && celery -A settings worker -l info --autoscale 1,10

beat:
	cd app && celery -A settings beat -l info

pytest:
	pytest ./app/tests --cov=app --cov-report html



#export PATH=$PATH:/usr/local/opt/rabbitmq/sbin
#
#Если потребуется перезагрузкить кролика:
#brew services restart rabbitmq

#sudo rabbitmqctl status
#sudo rabbitmqctl stop

#rabbitmqctl start_app
