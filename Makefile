docker = docker

build:
	$(docker) build -t vandorjw/django-assessment:local .

# Hi there,
# Are you missing a .env file?
# Please take a look at the 'test' command for common env variables.
run:
	$(docker) run --name local-django-assessment \
	-d \
	-p 5678:5000 \
	--env-file ./.env \
	vandorjw/django-assessment:local

clean:
	$(docker) stop local-django-assessment
	$(docker) rm local-django-assessment
	$(docker) stop local-django-assessment-test
	$(docker) rm local-django-assessment-test

push:
	microk8s.ctr image push vandorjw/django-assessment:latest

pull:
	microk8s.ctr image pull vandorjw/django-assessment:local

deploy:
	$(docker) build -t vandorjw/django-assessment:local .
	microk8s.ctr image push vandorjw/django-assessment:local
	microk8s.kubectl delete pods -l app=django-assessment
	microk8s.kubectl apply -f k8s/deployment.yml
	microk8s.kubectl apply -f k8s/service.yml
	microk8s.kubectl apply -f k8s/ingres.yml

status:
	microk8s.kubectl describe deployment django-assessment-deployment
	microk8s.kubectl describe service django-assessment-service
	microk8s.kubectl describe ingress django-assessment-ingres

logs:
	microk8s.kubectl logs -f -l app=django-assessment

pods:
	microk8s.kubectl get pods -l app=django-assessment

reload:
	microk8s.kubectl delete pods -l app=django-assessment

test:
	$(docker) run --name local-django-assessment-test \
	-e DJANGO_TESTING=true \
	-e DJANGO_SETTINGS_MODULE=demo.settings \
	-e PYTHONPATH=/app \
	localhost:32000/vandorjw/django-assessment \
	/usr/local/bin/django-admin.py test
