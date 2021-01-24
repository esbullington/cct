
VERSION=0.2.0
RELEASE=covidconnection-release-$(VERSION)
ZIPFILE=$(RELEASE).zip

REPODIR=$(HOME)/repos/covidconnection
TESTDIR=$(REPODIR)/tests

# docs
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = covidconnection
DOCSSOURCEDIR     = docs/source
DOCSBUILDDIR      = docs/build


# esp32
FIRMWARE = esp32-idf3-20210121-unstable-v1.13-274-g49dd9ba1a.bin


.PHONY: gh-pages package clean help Makefile write_flash erase_flash


write_flash:
	esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 firmware/$(FIRMWARE)

erase_flash:
	esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash

prebuild:
	rm -rf $(RELEASE)
	find covidconnection -type d -name  "__pycache__" -exec rm -r {} +
	mkdir -p $(RELEASE)
	mkdir -p $(RELEASE)/board
	cp README.md $(RELEASE)
	cp -r covidconnection $(RELEASE)/board/
	cp -r tools $(RELEASE)/

build:
	make prebuild
	find board/ -type f -not -name "*key*" -exec cp {} $(RELEASE)/board \;

buildwithkey:
	make prebuild
	cp -r board/ $(RELEASE)/

package:
	make build 
	@zip -r $(ZIPFILE) $(RELEASE) 1> /dev/null


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

html:
	@COVIDCONNECTION_VERSION=$(VERSION) $(SPHINXBUILD) -b html "$(DOCSSOURCEDIR)" "$(DOCSBUILDDIR)" $(SPHINXOPTS)

watchdocs:
	echo "Watching library and docs dirs to rebuild docs..."
	watchmedo shell-command docs/source covidconnection -w -W --pattern="*.py;*.rst" --recursive --command "echo \"rebuilding...\" && make html"

test:
	cd tests
	MICROPYPATH=$(MICROPYPATH):$(REPODIR) micropython $(TESTDIR)/integration_test.py
