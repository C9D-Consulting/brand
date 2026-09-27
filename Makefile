PY ?= python3

.PHONY: all icons covers themes html docx dist clean

all: icons covers themes html docx

icons:
	$(PY) generators/make_icons.py

covers:
	$(PY) generators/make_covers.py

themes:
	$(PY) generators/make_drive_themes.py

html:
	@mkdir -p renders/html
	$(PY) generators/c9d_html_build.py build generators/samples/html-sample.md renders/html/sample.html
	$(PY) generators/c9d_html_build.py check generators/samples/html-sample.md renders/html/sample.html

docx:
	@mkdir -p renders/docx
	$(PY) generators/c9d_docx_build.py generators/samples/html-sample.md renders/docx/sample.docx --check

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
