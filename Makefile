PYTHON=python3
PROJECT_NAME=nlptk

.PHONY: all clean test dist

all: test dist

test:
	$(PYTHON) -m unittest discover

clean:
	rm -rf build dist

dist:
	$(PYTHON) -m build

install:
	pip install --force-reinstall dist/*.tar.gz

build: clean build install
