PY ?= python3

.PHONY: all icons covers themes dist clean

all: icons covers themes

icons:
	$(PY) generators/make_icons.py

covers:
	$(PY) generators/make_covers.py

themes:
	$(PY) generators/make_drive_themes.py

dist:
	@mkdir -p dist
	@rm -rf dist/c9d-brand-skills-v$(shell cat VERSION)
	@mkdir -p dist/c9d-brand-skills-v$(shell cat VERSION)
	@cp -R c9d-consulting-brand c9d-brand-guard dist/c9d-brand-skills-v$(shell cat VERSION)/
	@cp docs/PACKAGE.md dist/c9d-brand-skills-v$(shell cat VERSION)/README.md
	@cd dist && zip -qr c9d-brand-skills-v$(shell cat VERSION).zip c9d-brand-skills-v$(shell cat VERSION)
	@rm -rf dist/c9d-brand-skills-v$(shell cat VERSION)
	@echo "built dist/c9d-brand-skills-v$(shell cat VERSION).zip"

clean:
	rm -rf dist
