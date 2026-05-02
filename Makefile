SHELL := /bin/bash

all: static

clean:
	find docs -mindepth 1 -not -name 'CNAME' -delete 2>/dev/null || true

dirs: clean
	mkdir -p docs/news
	mkdir -p docs/papers/bib

webpage: dirs
	python src/gen_webpage.py

static: webpage
	cp -r static/img/ docs/ 2>/dev/null || true
	cp -r static/css/ docs/ 2>/dev/null || true

test:
	python -m pytest -vv src/tests/

develop:
	livereload -p 8001 docs/
