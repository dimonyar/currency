SHELL := /bin/bash

manage_py := docker exec -it backend python app/manage.py

migrate:
	$(manage_py) migrate

shell:
	$(manage_py) shell_plus --print-sql

run:
	$(manage_py) runserver

uwsgi:
	cd app && uwsgi --http-socket 0.0.0.0:8000 --module settings.wsgi --threads 2 --workers 4 --daemonize=var/log/uwsgi/currency_uwsgi.log

worker:
	cd app && celery -A settings worker -l info -c 2

beat:
	cd app && celery -A settings beat -l info

flake8:
	docker exec -it backend flake8 app/

pytest:
	docker exec -it backend pytest ./app/tests --cov=app --cov-report html -vv && coverage report --fail-under=67

urls:
	$(manage_py) show_urls


#export PATH=$PATH:/usr/local/opt/rabbitmq/sbin
#
#Если потребуется перезагрузкить кролика:
#brew services restart rabbitmq

#sudo rabbitmqctl status
#sudo rabbitmqctl stop

#rabbitmqctl start_app

# fixture
# python app/manage.py dumpdata currency.rate > rate.json

# /usr/local/etc/nginx/nginx.conf
# sudo nginx -s quit && sudo nginx
# ps -ef | grep nginx



# ps ax|grep uwsgi
# killall uwsgi


# docker-compose up -d --build
# docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up -d --build
# docker-compose stop

# docker logs postgres
# docker inspect postgres