# Convenience targets. Requires: quarto, python, pip install -r requirements.txt

.PHONY: install gen check site pdf slides all preview clean

install:      ## install python deps
	pip install -r requirements.txt

check:        ## validate class metadata
	python scripts/check_meta.py

gen:          ## generate class pages + guide.qmd from meta.yml
	python scripts/build_pages.py

site: gen     ## build the HTML website into _site/
	quarto render

pdf: gen      ## build the combined PDF (needs LaTeX: quarto install tinytex)
	quarto render guide.qmd --to pdf

slides:       ## build the PPTX training deck
	quarto render slides/training.qmd --to pptx

all: check gen site pdf slides  ## build everything

preview: gen  ## live-preview the website
	quarto preview

clean:        ## remove build output
	rm -rf _site .quarto guide.pdf slides/training.pptx slides/training.html
