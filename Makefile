MAKE=/usr/bin/make
PREFIX=$(DESTDIR)/usr/
PYTHONLIB=$(PREFIX)/lib/python2.4/site-packages/
DRIZADIR=$(PYTHONLIB)/Driza/



all: uic rst

uic:
	$(MAKE) -C Driza/iuqt4/ui
	
rst:
	$(MAKE) -C Driza/ayuda

.DEFAULT:
	python setup.py $@

