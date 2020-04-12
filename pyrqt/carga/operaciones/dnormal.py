#!/usr/bin/python
# -*- coding: utf-8 -*-

#dnormal.py Distribucion Normal

#Copyright (C) 2006  Inmaculada Luengo Merino, Néstor Arocha Rodríguez
#This file is part of Driza.
#
#Driza is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#Driza is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Driza; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

nombre=u"Distribución Normal"
descripcion="BLABLABLA"
tipo="Distribucion"

def funcion(dato,opciones):  
    from rpy import r  #pylint: disable=import-error
    diccionario={}
    if "Cuantiles" in opciones:
        if opciones["Cuantiles"][u"DirecciónCola"]=='izquierda':
            sentido=True
        else:
            sentido=False
        diccionario["cuantiles"]=r.qnorm([float(opciones["Cuantiles"]["Probabilidad"])],mean=float(opciones["Cuantiles"]["Media"]),sd=float(opciones["Cuantiles"][u"Desviación"]),lower_tail=sentido)
    if "Probabilidades" in opciones:
        if opciones["Probabilidades"][u"DirecciónCola"]=='izquierda':
            sentido=True
        else:
            sentido=False
        diccionario["probabilidades"]=r.pnorm([float(opciones["Probabilidades"]["Valores"])],mean=float(opciones["Probabilidades"]["Media"]),sd=float(opciones["Probabilidades"][u"Desviación"]),lower_tail=sentido)
    if u"Gráfica" in opciones:
        import random
        nombrefichero="/tmp/driza"+str(random.randint(1,99999))+".png"
        diccionario["ruta"]=nombrefichero
        r.png(nombrefichero) #Directorio temporal de la config
        lista=r.seq(-3.291, 3.291, length=100)
        if opciones[u"Gráfica"]["Tipografica"]=="Densidad":
            etiquetay="Densidad"
            mifuncion=r.dnorm
        else:
            etiquetay="Probabilidad acumulada"
            mifuncion=r.pnorm
        r.plot(lista, mifuncion(lista, mean=float(opciones[u"Gráfica"]["Media"]), sd=float(opciones[u"Gráfica"][u"Desviación"])), xlab="x", ylab=etiquetay, main=r.expression(r.paste("Normal Distribution: ", "mu", " = 0, ", "sigma", " = 1")), type="l")
        r.abline(h=0, col="gray")
        r.dev_off()
    return diccionario

def initresultado(resultado,opciones):
    """Inicializa al objeto resultado, añadiendole lo que crea conveniente"""
    resultado.addTexto("cuantiles")
    resultado["cuantiles"].settitulo("Estudio de cuantiles")
    resultado.addTexto("probabilidades")
    resultado["probabilidades"].settitulo("Estudio de probabilidades")
    resultado.addImagen("grafica")
    resultado["grafica"].settitulo(u"Gráfica distribución normal")


def interfazresultado(resultado,diccionario,floatrender=None):
    """Este método dice como introducir los datos en la tabla"""
    if "cuantiles" in diccionario:
        resultado["cuantiles"].set(diccionario["cuantiles"])
    if "probabilidades" in diccionario:
        resultado["probabilidades"].set(diccionario["probabilidades"])
    if "ruta" in diccionario:
        resultado["grafica"].set(diccionario["ruta"])


diccionario1= {"nombre":"Media","tipo":"EntradaTexto"}
diccionario2= {"nombre":u"Desviación","tipo":"EntradaTexto"}
listacuantilesprob=[diccionario1,diccionario2]

widget={"tipo":"Distribucion","opcionescomun":listacuantilesprob}


def comprobarentrada(opciones):  
    pass


def funcionprincipal(): pass
def funcionchequeocondiciones(interfazdato): return False
def funcionchequeoentradausuario(opciones): return False
definicionresultado = []
tipo = "Casos" #FIXME: Tipo incorrecto
etiquetas = ["Otros"]
widget = {"tipo":"Variable", "opciones":[]}
