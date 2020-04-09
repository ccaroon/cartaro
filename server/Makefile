test:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	nosetests -v -s tests/*

test1:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	nosetests -v -s tests/model/test_base.py -m test_load

cover:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	nosetests -v -s tests/* \
			--with-coverage \
			--cover-erase \
			--cover-html \
			--cover-inclusive \
			--cover-xml \
			--cover-package cartaro

dev:
	. ./venv/bin/activate; \
	CARTARO_DOC_PATH=${HOME}/Documents/Cartaro \
	CARTARO_ENV=dev       \
	FLASK_ENV=development \
	FLASK_APP=cartaro     \
	flask run -p 4242

clean:
	rm -f `find . -name "*.pyc"`
	rm -f tests/tmp/*.json
	rm -rf .coverage coverage.xml cover/

.PHONY: test cover dev clean
