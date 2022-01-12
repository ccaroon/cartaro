usage:
	@echo "* clean: Clean up a bit."
	@echo "* cover: Run Code Coverage"
	@echo "* cover-file: Run Code Coverage for a single file"
	@echo "* dev: Start development server"
	@echo "* dist: Create distribution directory"
	@echo "* dist-clean: Clean up 'dist' droppings."
	@echo "* package: Build distribution package"
	@echo "* test: Run Unit Tests"
	@echo "* test-file: Run Unit Tests for a single file"

test:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	CARTARO_CFG_PATH=../tests/data \
	nosetests -v -s tests/*

test-file:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	CARTARO_CFG_PATH=../tests/data \
	nosetests -v -s $(FILE)

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
			--cover-min-percentage 95 \
			--cover-package cartaro

cover-file:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	CARTARO_CFG_PATH=../tests/data \
	nosetests -v -s $(FILE) \
			--with-coverage \
			--cover-erase \
			--cover-html \
			--cover-inclusive \
			--cover-xml \
			--cover-package cartaro

dev:
	CARTARO_DOC_PATH=${HOME}/Documents/Cartaro \
	CARTARO_ENV=dev       \
	FLASK_ENV=development \
	FLASK_APP=cartaro     \
	flask run -p 7777

bin/python:
	cp `which python` bin

dist: bin/python requirements-prod.txt $(shell find cartaro -name "*.py")
	rm -rf dist/
	pip install --target ./dist -r requirements-prod.txt
	mkdir -p dist/bin
	cp bin/python dist/bin
	cp -a cartaro dist/

package: dist
	cd dist && zip -r ../cartaro-server.zip * && cd ..

clean:
	rm -f `find . -name "*.pyc"`
	rm -f tests/tmp/*.json
	rm -rf .coverage coverage.xml cover/
	rm -f cartaro-server.zip

dist-clean: clean
	rm -rf dist/

.PHONY: usage test test-file cover cover-file dev dist package clean dist-clean
