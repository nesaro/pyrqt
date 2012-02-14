#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007 Néstor Arocha Rodríguez, Inmaculada Luengo Merino
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

"""Operación jicuadrado"""

nombre="Ji Cuadrado"
tipo="Calculo"
etiquetas=["Bondad de ajuste"]
distribucioncontraste={
        "nombre":u"Distribución",
        "tipo":"SeleccionSimple",
        "opciones":["Uniforme"]}
widget={"tipo":"Variable","opciones":[distribucioncontraste]}
definicionresultado = [
        {"tipo":"Tabla","nombre":"Ji cuadrado","cabecera":["Variable",u"Significación"]}]

def funcionprincipal(dato,variable,opciones):
    from rpy import r
    lista=dato.query(variable)
    num=len(lista)
    numcasos=len(list(r.table(lista)))
    total=0
    diccionario = {}
    diccionario["Ji cuadrado"] = {}
    #MEJOR CONDICION TODAVIA = Numero de valores/Numero de datos > 0.15
    #TODO: Cambiar por la "mejor condicion"
    if numcasos<30: 
        if opciones[u"Distribución"]=="Uniforme":
            distribucion=r.runif(numcasos,1./numcasos,1./numcasos)
        resultado=r.chisq_test(list(r.table(lista)),p=distribucion)
    else:
        rango=r.range(lista)
        limiteinferior=rango[0]-0 #TODO: Revisar precisión
        limitesuperior=rango[1]+0
        longitudrango=limitesuperior-limiteinferior
        numdivisiones=int(0.15*num)
        divisor=longitudrango/numdivisiones
        listaobtenida=[0 for x in range(numdivisiones)]
        for reg in lista:
            posicion=int(float(reg-limiteinferior-1)/divisor)
            if posicion>=numdivisiones: posicion=numdivisiones-1
            listaobtenida[posicion]+=1
        distribucion=r.runif(numdivisiones,1./numdivisiones,1./numdivisiones)
        resultado=r.chisq_test(listaobtenida,p=distribucion)

    diccionario["Ji cuadrado"]["Variable"] = str(variable)
    diccionario["Ji cuadrado"][u"Significación"]=resultado["p.value"]
    return diccionario


def funcionchequeoentradausuario(opciones):  
    return True

def funcionchequeocondiciones(interfazdato):
    return True

