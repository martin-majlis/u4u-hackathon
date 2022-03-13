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
