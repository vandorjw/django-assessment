build:
	docker build -t localhost:32000/vandorjw/django-assessment .

run:
	docker run --name local-django-assessment \
	-d \
	-p 5000:5000 \
	--env-file ./.env \
	localhost:32000/vandorjw/django-assessment

clean:
	docker stop local-django-assessment
	docker rm local-django-assessment

push:
	docker push localhost:32000/vandorjw/django-assessment

deploy:
	kubectl apply -f k8s/deployment.yml

test:
	docker run --name local-django-assessment-test \
	-e DJANGO_TESTING=True \
	-e DJANGO_SETTINGS_MODULE=demo.settings \
	-e PYTHONPATH=/app \
	localhost:32000/vandorjw/django-assessment \
	/usr/local/bin/django-admin.py check

stop:
	docker stop local-django-assessment-test
	docker rm local-django-assessment-test
