tests:
	@nosetests --with-coverage --cover-package skeleton -v

clean:
	@find . -type f -name \*.pyc -exec rm {} \;

pep8:
	@pep8 skeleton
