PROG = vprincipal.html
MAKE=/usr/bin/make
all: $(PROG) 

%.html: %.rst
	rst2html --no-xml-declaration $< > $@

clean:
	rm *.html

