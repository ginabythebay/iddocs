
NAME := iddocs
VERSION := v0.0.40

PYTHON=venv/bin/python

.PHONY: createsuperuser freeze genkey makemigrations migrate serve shell test dist release stage prod

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

# TODO(gina) figure out how to get this working again.  It stopped working when I switched to mysql
test: venv
	$(PYTHON) manage.py test

dist: test venv
	@rm -rf dist && mkdir dist
	git archive master | bzip2 >dist/source.tar.bz2
	(cd $(shell pwd)/dist && shasum -a 512 source.tar.bz2 > source.sha512);

release: dist
	@latest_tag=$$(git describe --tags `git rev-list --tags --max-count=1`); \
	comparison="$$latest_tag..HEAD"; \
	if [ -z "$$latest_tag" ]; then comparison=""; fi; \
	changelog=$$(git log $$comparison --oneline --no-merges); \
	github-release ginabythebay/$(NAME) $(VERSION) "$$(git rev-parse --abbrev-ref HEAD)" "**Changelog**<br/>$$changelog" 'dist/*'; \
	git pull

stage: venv
	fab stage:$(VERSION)

prod: venv
	fab prod:$(VERSION)

venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

venv: venv/bin/activate
