test:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	nosetests -v -s tests/

cover:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	nosetests -v -s tests/ \
			--with-coverage \
			--cover-erase \
			--cover-html \
			--cover-inclusive \
			--cover-xml \
			--cover-package server

dev:
	. ./venv/bin/activate; \
	CARTARO_DOC_PATH=/home/ccaroon/Documents/Cartaro \
	CARTARO_ENV=dev
	FLASK_ENV=development \
	flask run -p 4242

clean:
	rm -f `find . -name "*.pyc"`
	rm -f tests/tmp/*.json

.PHONY: test cover dev clean
