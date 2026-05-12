PYTHON ?= python3
FILE ?= maps/test/00_TEST.txt


install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) main.py $(FILE)

debug:
	$(PYTHON) -m pdb main.py $(FILE)

clean:
	rm -rf __pycache__ .mypy_cache */__pycache__

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict