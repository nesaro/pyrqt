MAKE=/usr/bin/make
PREFIX=$(DESTDIR)/usr/



all: uic rst

uic:
	$(MAKE) -C pyrqt/iuqt4/ui
	
rst:
	$(MAKE) -C pyrqt/ayuda

.DEFAULT:
	python setup.py $@

