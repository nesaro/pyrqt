#!/usr/bin/python
# -*- coding: utf-8 -*-

#comppropsim.py: Ejecuta una comparacion de proporciones simple

#Copyright (C) 2006  Inmaculada Luengo Merino, Néstor Arocha Rodríguez
#This file is part of pyrqt.
#
#pyrqt is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#pyrqt is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pyrqt; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

nombre=u"Comparación de proporciones simple"
tipo="Calculo"
diccionarioalternativa={ "nombre":u"Hipótesis alternativa", "tipo":"SeleccionSimple", "opciones":["<",">","!="]}
significacion={"nombre":u"Significación","tipo":"EntradaTexto"}
mediaobjetivo={"nombre":"Proporcion objetivo","tipo":"EntradaTexto"}
widget={"tipo":"ProporcionSimple","opciones":[mediaobjetivo,significacion,diccionarioalternativa]}

def funcion(dato, variable, caso, opciones):  
    from rpy import r #pylint: disable=import-error
    diccionario = {}
    lavar=variable[0]
    condicion=variable[1]
    micondicion=lavar+"="+condicion #La cadena quedara formada como PESO=75
    lista1=dato.query(lavar,caso,micondicion)
    lista2=dato.query(lavar,caso) #Lista sin condicion
    if opciones[u"Hipótesis alternativa"]==">":
        lateral="greater"
    elif opciones[u"Hipótesis alternativa"]=="<":
        lateral="less"
    else:
        lateral="two.sided"
    diccionario=r.prop_test(len(lista1),len(lista2),alternative=lateral,p=float(opciones["Proporcion objetivo"]),conf_level=float(opciones[u"Significación"])/100)
    diccionario["confianza"]=float(opciones[u"Significación"])/100
    return diccionario

def initresultado(resultado,opciones):
    """Inicializa al objeto resultado, añadiendole lo que crea conveniente"""
    resultado.addTablaSimple("resultado")
    lista=[]
    if opciones["caso"]:
        lista.append("Caso")
    lista.append("Elemento")
    lista+=[u"Hipótesis alternativa","Intervalo de confianza","Valor p obtenido","Conclusion"]
    resultado["resultado"].settitulo(lista)


def interfazresultado(resultado,listaopciones,floatRender=None):
    """Este método dice como introducir los datos en la tabla"""
    lista=[]
    variable=listaopciones[0]
    caso=listaopciones[1]
    if caso:
        lista.append(caso)
    diccionario=listaopciones[2]
    lista.append(variable[1])
    lista.append(diccionario["alternative"])
    lista.append(diccionario["conf.int"])
    lista.append(diccionario["p.value"])
    if (diccionario["p.value"] < diccionario["confianza"]): 
        texto=u"Hay evidencias estadísticas de que la hipótesis alternativa es válida"
    else: 
        texto=u"No hay evidencias estadísticas de que la hipótesis alternativa sea válida"
    lista.append(texto)
    resultado["resultado"].set(variable[0],lista)


def comprobarentrada(opciones):  
    if not opciones.has_key(u"Significación") or not opciones.has_key("Proporcion objetivo"):
        from pyrqt.excepciones import OpcionesIncorrectaException
        raise OpcionesIncorrectaException



def funcionprincipal(): pass
def funcionchequeocondiciones(interfazdato): return False
def funcionchequeoentradausuario(opciones): return False
definicionresultado = []
tipo = "Casos" #FIXME: Tipo incorrecto
etiquetas = ["Otros"]
widget = {"tipo":"Variable", "opciones":[]}
