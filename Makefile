
VERSION=0.2.7
RELEASE=cct-release-$(VERSION)
ZIPFILE=$(RELEASE).zip

REPODIR=$(HOME)/repos/cct
TESTDIR=$(REPODIR)/tests

# docs
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = cct
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
	find cct -type d -name  "__pycache__" -exec rm -r {} +
	mkdir -p $(RELEASE)
	mkdir -p $(RELEASE)/firmware
	mkdir -p $(RELEASE)/board
	cp README.md $(RELEASE)
	cp -r cct $(RELEASE)/board/
	cp -r tools $(RELEASE)/
	cp -r .vscode $(RELEASE)/
	cp .pylintrc $(RELEASE)/.pylintrc
	cp -r stubs $(RELEASE)/
	cp firmware/$(FIRMWARE) $(RELEASE)/firmware/esp32.bin

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
	make html
	rm -rf /tmp/gh-pages
	cp -r $(DOCSBUILDDIR) /tmp/gh-pages
	git checkout gh-pages
	rm -rf * && cp -rT /tmp/gh-pages ./ && rm -rf /tmp/gh-pages && git add . && git commit -m "Updated gh-pages" && git push && git checkout master

# Put it first so that "make" without argument is like "make help".
docshelp:
	@$(SPHINXBUILD) -M help "$(DOCSSOURCEDIR)" "$(DOCSBUILDDIR)" $(SPHINXOPTS) $(O)

autodoc:
	cd $(DOCSSOURCEDIR)
	sphinx-apidoc -f -o $(DOCSSOURCEDIR) ../cct

html:
	@COVIDCONNECTION_VERSION=$(VERSION) $(SPHINXBUILD) -b html "$(DOCSSOURCEDIR)" "$(DOCSBUILDDIR)" $(SPHINXOPTS)

watchdocs:
	echo "Watching library and docs dirs to rebuild docs..."
	watchmedo shell-command docs/source cct -w -W --pattern="*.py;*.rst" --recursive --command "echo \"rebuilding...\" && make html"

test:
	cd tests
	micropython $(TESTDIR)/integration_test.py
