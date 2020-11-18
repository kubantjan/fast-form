setup:
	pip install pip-tools
	pip-sync

setup-dev:
	pip install pip-tools
	pip-sync requirements.txt dev-requirements.txt
	pre-commit install

upload_to_pypi:
	pip install twine
	python setup.py sdist
	twine upload dist/*
