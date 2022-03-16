OPEN=xdg-open

PROJECT_DIR=.
TEST_DIR=tests

checks: mypy test

mypy:
	mypy $(PROJECT_DIR) $(TEST_DIR)

test: test-ci

test-ci:
	pytest \
		--cov=$(PROJECT_DIR) \
		-v \
		--ignore lindat_translation_master \
		--ignore hunalign-1.1

coverage:
	coverage html -d coverage_html
	$(OPEN) coverage_html/index.html

test-and-coverage: test coverage

pre-commit-all:
	pre-commit run -a -v || git diff

pre-commit-install:
	pre-commit install

install-all: dep-install pre-commit-install

dep-install: dep-install-run dep-install-dev external-install

dep-install-run:
	pip install -r requirements.txt

dep-install-dev:
	pip install -r requirements-dev.txt

external-install:
	if [ ! $$( which wget ) ]; then \
		apt-get install wget; \
	fi
	if [ ! -d lindat_translation_master ]; then \
		wget \
			https://github.com/ufal/lindat-translation/archive/refs/heads/master.zip \
			-O lindat_translation_master.zip; \
		unzip lindat_translation_master.zip; \
		mv lindat-translation-master lindat_translation_master; \
	fi;

run-extract-ukrainer:
	python ukrainer.py

combine-sentences:
	find data/ukrainer-processed/ -name 'cs_sentences.txt' -exec cat {} \; > data/cs_sentences.txt
	find data/ukrainer-processed/ -name 'ua_sentences.txt' -exec cat {} \; > data/ua_sentences.txt

run-hunalign:
	hunalign-1.1/src/hunalign/hunalign hunalign-1.1/data/null.dic data/cs_sentences.txt data/ua_sentences.txt -text > data/cs-ua-hunaligned_sentences.txt


stats-sentences-extracted:
	wc data/*_sentences.txt
