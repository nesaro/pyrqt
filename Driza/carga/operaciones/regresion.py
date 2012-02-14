#!/usr/bin/python
# -*- coding: utf-8 -*-


#Copyright (C) 2006  Néstor Arocha Rodríguez, Inmaculada Luengo Merino
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

"""regresion.py Operación Regresión"""


nombre=u"Regresión"
tipo="Calculo"
widget={"tipo":"CalculoDoble","opciones":{}}

def funcion(dato,variable,caso,opciones):  # Cambiar cosa por caso
    from rpy import r
    variable1 = variable[0]
    variable2 = variable[1]
    lista1=dato.query(variable1,caso)
    lista2=dato.query(variable2,caso)
    #lista2=[float(x) for x in dato.getCol(variable2,caso=caso)]
    resultadoprueba=r.lm(r("y ~ x"),data=r.data_frame(x=lista1, y=lista2))
    sumario=r.summary_lm(resultadoprueba,True)
    anova=r.anova_lm(resultadoprueba)
    #resultadoprueba=r.lsfit(lista1,lista2)
    midiccionario={"resultado":resultadoprueba,"sumario":sumario,"anova":anova}
    return midiccionario

def initresultado(resultado,opciones):
    """Inicializa al objeto resultado, añadiendole lo que crea conveniente"""
    resultado.addTablaDoble("r")
    resultado.addTablaDoble("principal")
    resultado.addTablaDoble("anova")
    resultado.titulo=u"Regresión Lineal"
    lista=[]
    if opciones["caso"]:
        lista.append("Caso")
    lista+=["coeficiente r","coeficiente r^2","Significacion"]
    resultado["principal"].settitulo(lista)
    resultado["r"].settitulo(["r","r^2","significacion"])
    resultado["anova"].settitulo(["F","df","significacion"])


def interfazresultado(resultado,listaopciones,floatrender=None):
    """Este método dice como introducir los datos en la tabla"""
    #Falta coeficiente de correlacion r
    #Falta coeficiente de determinacion r^2
    #Afinar parametros de la recta
    #Significacion
    #Hay un anova sipmple que determina si la recta se cumple
    lista=[]
    variables=listaopciones[0]
    caso=listaopciones[1]
    diccionario=listaopciones[2]
    if caso:
        lista.append(caso)
    #lista+=[diccionario['coefficients']['X'],diccionario['coefficients']['Intercept']]
    lista+=["",floatrender.render(diccionario["sumario"]["r.squared"]),str(diccionario)]
    resultado["principal"].set(variables,lista)
    resultado["r"].set(variables,[""])
    resultado["anova"].set(variables,[""])



def comprobarentrada(opciones):  
    pass


def funcionprincipal(): pass
def funcionchequeocondiciones(interfazdato): return False
def funcionchequeoentradausuario(opciones): return False
definicionresultado = []
tipo = "Casos" #FIXME: Tipo incorrecto
etiquetas = ["Otros"]
widget = {"tipo":"Variable", "opciones":[]}
