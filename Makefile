
VERSION=0.01
RELEASE=covidconnection-release-$(VERSION)
ZIPFILE=$(RELEASE).zip

# docs
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = covidconnection
DOCSSOURCEDIR     = docs/source
DOCSBUILDDIR      = docs/build


.PHONY: gh-pages package clean help Makefile


build:
	find covidconnection -type d -name  "__pycache__" -exec rm -r {} +
	mkdir -p $(RELEASE)
	cp README.md $(RELEASE)
	cp -r example_program $(RELEASE)/
	cp -r covidconnection $(RELEASE)/example_program
	cp -r scripts $(RELEASE)/

package:
	make build
	zip -r $(ZIPFILE) $(RELEASE)


clean:
	rm -f $(ZIPFILE)
	rm -rf $(RELEASE)

gh-pages:
	rm -rf /tmp/gh-pages
	cp -r $(DOCSBUILDDIR)/html /tmp/gh-pages
	git checkout gh-pages
	cd .. && rm -rf * && cp -r /tmp/gh-pages/* ./ && rm -rf /tmp/gh-pages && git add . && git commit -m "Updated gh-pages" && git push && git checkout master

# Put it first so that "make" without argument is like "make help".
docshelp:
	@$(SPHINXBUILD) -M help "$(DOCSSOURCEDIR)" "$(DOCSBUILDDIR)" $(SPHINXOPTS) $(O)

autodoc:
	cd $(DOCSSOURCEDIR)
	sphinx-apidoc -f -o $(DOCSSOURCEDIR) ../covidconnection

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(DOCSSOURCEDIR)" "$(DOCSBUILDDIR)" $(SPHINXOPTS) $(O)
