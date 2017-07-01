VIRTUALENV = virtualenv --python=python3
VENV := $(shell echo $${VIRTUAL_ENV-.venv})
PYTHON = $(VENV)/bin/python
INSTALL_STAMP = $(VENV)/.install.stamp
TEMPDIR := $(shell mktemp -d)

.IGNORE: clean distclean maintainer-clean
.PHONY: all install virtualenv tests

OBJECTS = .venv .coverage

all: install
install: $(INSTALL_STAMP)
$(INSTALL_STAMP): $(PYTHON) setup.py
	$(VENV)/bin/pip install -U pip
	$(VENV)/bin/pip install -Ur dev-requirements.txt
	$(VENV)/bin/pip install -Ue .
	touch $(INSTALL_STAMP)

build-requirements:
	$(VIRTUALENV) $(TEMPDIR)
	$(TEMPDIR)/bin/pip install -Ue .
	$(TEMPDIR)/bin/pip freeze | grep -v -- '^-e' > requirements.txt

virtualenv: $(PYTHON)
$(PYTHON):
	$(VIRTUALENV) $(VENV)

tests-once: install
	$(VENV)/bin/tox -e py35

tests:
	$(VENV)/bin/tox

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d | xargs rm -fr

distclean: clean
	rm -fr *.egg *.egg-info/

maintainer-clean: distclean
	rm -fr $(OBJECTS) .tox/ dist/ build/
