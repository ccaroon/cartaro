help:
	@echo "* clean: Clean up a bit."
	@echo "* cover: Run Code Coverage"
	@echo "* cover-module: Run Code Coverage for a single test module"
	@echo "* dev: Start development server"
	@echo "* dist: Create distribution directory"
	@echo "* dist-clean: Clean up 'dist' droppings."
	@echo "* package: Build distribution package"
	@echo "* test: Run Unit Tests"
	@echo "* test-module: Run Unit Tests for a single test module"

test:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	CARTARO_CFG_PATH=../tests/data \
	nose2 -v -s tests

test-module:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	CARTARO_CFG_PATH=../tests/data \
	nose2 -v $(MODULE)

cover:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	CARTARO_CFG_PATH=../tests/data \
	nose2 -v -s tests \
			--with-coverage	\
			--coverage-report html \
			--coverage-report term
			# --cover-min-percentage 95 \

cover-module:
	CARTARO_ENV=test \
	CARTARO_DOC_PATH=tests/tmp \
	CARTARO_CFG_PATH=../tests/data \
	nose2 -v $(MODULE) \
			--with-coverage \
			--coverage-report html \
			--coverage-report term
			# --cover-min-percentage 95 \

dev:
	CARTARO_DOC_PATH=${HOME}/Documents/Cartaro \
	CARTARO_ENV=dev       \
	FLASK_ENV=development \
	FLASK_APP=cartaro     \
	flask run -p 7777

bin/python:
	cp `pyenv which python` bin

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
	rm -rf .coverage htmlcov
	rm -f cartaro-server.zip

dist-clean: clean
	rm -rf dist/

.PHONY: usage test test-file cover cover-file dev package clean dist-clean
