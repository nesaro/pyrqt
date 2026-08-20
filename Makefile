MAKE=make
PREFIX=$(DESTDIR)/usr/



all: uic rst

uic:
	$(MAKE) -C pyrqt/iuqt5/ui
	
rst:
	$(MAKE) -C pyrqt/ayuda

translations:
	pylupdate5 pyrqt/iuqt5/ui/*.ui -ts driza_es_ES.ts

.DEFAULT:
	python setup.py $@

