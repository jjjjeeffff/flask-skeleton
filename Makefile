APP_NAME?=skeleton

tests:
	@nosetests --with-coverage --cover-package skeleton -v

clean:
	@find . -type f -name \*.pyc -exec rm {} \;

pep8:
	@pep8 skeleton

rename:
	@perl -e "s/skeleton/$(APP_NAME)/g;" -pi $$(find . -type f)
	@mv skeleton $(APP_NAME)
