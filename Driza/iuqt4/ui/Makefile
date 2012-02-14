PROG = dbuscar.py dcasos.py dconfig.py dcrevar.py dsplash.py doperaciones.py dfiltrado.py wconfig1.py vprincipal.py vsalida.py
#dimportartexto.py
MAKE=/usr/bin/make
all: $(PROG) 

%.py: %.ui
	pyuic4 $< -o $@

clean:
	rm *.pyc ui*.py *~

