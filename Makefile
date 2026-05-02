SHELL := /bin/bash

all: static

clean:
	rm -rf output

dirs: clean
	mkdir -p output/news
	mkdir -p output/papers/bib

webpage: dirs
	python src/gen_webpage.py

static: webpage
	cp -r static/img/ output/ 2>/dev/null || true
	cp -r static/css/ output/ 2>/dev/null || true

test:
	python -m pytest -vv src/tests/

develop:
	livereload -p 8001 output/
