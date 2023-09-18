# Phony targets represent actions rather than files
.PHONY: all bump build release

# Get the latest git tag
LATEST_TAG = $(shell git describe --tags --abbrev=0)

# Specify which level to increment
BUMP_LEVEL ?= patch
# Parse tag parts: major, minor, and patch
MAJOR := $(shell echo $(LATEST_TAG) | cut -d'.' -f1)
MINOR := $(shell echo $(LATEST_TAG) | cut -d'.' -f2)
PATCH := $(shell echo $(LATEST_TAG) | cut -d'.' -f3)

all: build push

bump:
	@echo "Version $(MAJOR).$(MINOR).$(PATCH)"
	@echo "Bumping $(BUMP_LEVEL) version..."
	@if [ "$(BUMP_LEVEL)" = "major" ]; then \
		NEW_TAG="$$(($$((10#$(MAJOR))) + 1)).0.0"; \
	elif [ "$(BUMP_LEVEL)" = "minor" ]; then \
		NEW_TAG="$(MAJOR).$$((10#$(MINOR) + 1)).0"; \
	elif [ "$(BUMP_LEVEL)" = "patch" ]; then \
		NEW_TAG="$(MAJOR).$(MINOR).$$((10#$(PATCH) + 1))"; \
	else \
		echo "Invalid BUMP_LEVEL specified. Choose from 'major', 'minor', or 'patch'."; \
		exit 1; \
	fi; \
	echo "New tag: $$NEW_TAG"; \
	git tag $$NEW_TAG; \
	git push origin $$NEW_TAG

build:
	rm -rfv dist/*
	python -m build

release: build
	python -m twine upload --repository kaslcred dist/*
