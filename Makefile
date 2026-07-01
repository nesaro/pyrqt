MAKE=make
PREFIX=$(DESTDIR)/usr/



all: uic rst

uic:
	$(MAKE) -C pyrqt/iuqt5/ui
	
rst:
	$(MAKE) -C pyrqt/ayuda

.DEFAULT:
	python setup.py $@

