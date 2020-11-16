#(install dependency python manager, install dependencies, add pre-commit hook that cleans up notebooks upon a commit)
setup:
	pip install pip-tools
	pip-sync