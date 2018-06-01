#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007  Néstor Arocha Rodríguez, Inmaculada Luengo Merino
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

#FIXME: MAL, los querys no pueden ser independientes

"""Diagrama de dispersión"""

nombre=u"Diagrama de dispersión"
tipo="Calculo"
etiquetas = ["Descriptivos"]
widget = {"tipo":"VariableVariable","opciones":[] }
definicionresultado = [{"tipo":"Imagen","nombre":u"Diagrama de dispersión"}]

def funcionprincipal(dato,variables,opciones): 
    from rpy import r  #pylint: disable=import-error
    diccionario = {}
    diccionario[u"Diagrama de dispersión"]={}
    variable1=variables[0]
    variable2=variables[1]
    lista1=dato.query(variable1)
    lista2=dato.query(variable2)
    import random
    nombrefichero="/tmp/driza"+str(random.randint(1,99999))+".png"
    diccionario[u"Diagrama de dispersión"]["ruta"] = nombrefichero
    r.png(nombrefichero) #Directorio temporal de la config
    #r.require("car")
    #r.scatterplot(lista1,lista2,reg_line=False,labels=False,smooth=False,span=0.5,xlab=variable1,ylab=variable2)
    r.pairs([lista1,lista2])
    r.dev_off()
    return diccionario

def funcionchequeoentradausuario(opciones):  
    return True

def funcionchequeocondiciones(interfazdato):
    return True
