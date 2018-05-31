PROG =  dayuda.py dbuscar.py dcasos.py dconfig.py dcrevar.py dsplash.py dimportartexto.py doperaciones.py dfiltrado.py wconfig1.py vprincipal.py vsalida.py
MAKE=/usr/bin/make
all: $(PROG) 

%.py: %.ui
	pyuic -p 4 $< -o $@

clean:
	rm $(PROG) *.pyc ui*.py *~

