test:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	CARTARO_CFG_PATH=../tests/data \
	nosetests -v -s tests/*

test-file:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	CARTARO_CFG_PATH=../tests/data \
	nosetests -v -s tests $(FILE)

cover:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	CARTARO_CFG_PATH=../tests/data \
	nosetests -v -s tests/* \
			--with-coverage \
			--cover-erase \
			--cover-html \
			--cover-inclusive \
			--cover-xml \
			--cover-package cartaro

cover-file:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	CARTARO_CFG_PATH=../tests/data \
	nosetests -v -s tests $(FILE) \
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
	flask run -p 7777

clean:
	rm -f `find . -name "*.pyc"`
	rm -f tests/tmp/*.json
	rm -rf .coverage coverage.xml cover/

.PHONY: test cover dev clean
