
PYTHON=venv/bin/python

.PHONY: createsuperuser freeze genkey makemigrations migrate serve shell test

createsuperuser: venv
	$(PYTHON) manage.py createsuperuser

freeze: venv
	pip freeze > requirements.txt

genkey: venv
	@$(PYTHON) -c "import string,random; uni=string.ascii_letters+string.digits+string.punctuation; print repr(''.join([random.SystemRandom().choice(uni) for i in range(random.randint(45,50))]))"

makemigrations: venv
	$(PYTHON) manage.py makemigrations

migrate: venv
	$(PYTHON) manage.py migrate

serve: venv
	$(PYTHON) manage.py runserver

shell: venv
	$(PYTHON) manage.py shell

test: venv
	$(PYTHON) manage.py test

venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

venv: venv/bin/activate
