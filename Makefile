CONDA_ENV=fast-form

conda-create:
	conda env create -f conda.yml --name $(CONDA_ENV)


setup:
	python -m pip install --upgrade setuptools
	python setup.py install


setup-dev:
	pip install -e .[dev]