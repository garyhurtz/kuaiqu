# setup variables
PYTHON := $(shell which python)

# generate requirements.txt using only top-level packages
freeze:
	pipdeptree -f --python $(PYTHON) --warn silence | grep -E '^[a-zA-Z0-9\-]+' > requirements.txt
