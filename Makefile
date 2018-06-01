MAKE=/usr/bin/make
PREFIX=$(DESTDIR)/usr/
PYTHONLIB=$(PREFIX)/lib/python2.4/site-packages/



all: uic rst

uic:
	$(MAKE) -C pyrqt/iuqt4/ui
	
rst:
	$(MAKE) -C pyrqt/ayuda

.DEFAULT:
	python setup.py $@

