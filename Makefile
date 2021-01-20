
VERSION="0.01"

RELEASE="covidconnection-release-$(VERSION)"

package:
	mkdir -p $(RELEASE)
	cp -r example_program/* $(RELEASE)/
	cp -r covidconnection $(RELEASE)/
	cp -r scripts $(RELEASE)/
	zip -r $(RELEASE).zip $(RELEASE)
	rm -rf $(RELEASE)
