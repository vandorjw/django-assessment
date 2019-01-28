build:
	docker build -t localhost:32000/vandorjw/django-assessment .

start:
	docker run -d -p 5000:5000 --name local-django-assessment localhost:32000/vandorjw/django-assessment

stop:
	docker stop local-django-assessment
	docker rm local-django-assessment