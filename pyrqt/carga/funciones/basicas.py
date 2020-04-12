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

"""Funciones básicas"""

from pyrqt.datos.funciones import Funcion

class Default(Funcion):
    """Devuelve el valor por defecto de la variable de entrada"""
    def __init__(self):
        nombre = "Default(x)"
        Funcion.__init__(self, nombre)

    def __call__(self, instanciavariable):
        return instanciavariable.tvariable.valorpordefecto
    

class Ln(Funcion):
    """Devuelve el Logaritmo neperiano de la variable pasada"""
    def __init__(self):
        nombre = "Ln(x)"
        Funcion.__init__(self, nombre)
    def __call__(self, instanciavariable):
        import math
        return math.log(float(instanciavariable))
    
class Exp(Funcion):
    """Devuelve e elevado a la variable pasada"""
    def __init__(self):
        nombre = "Exp(x)"
        Funcion.__init__(self, nombre)

    def __call__(self, instanciavariable):
        import math
        return math.exp(float(instanciavariable))
    
class Pow(Funcion):
    """Devuelve A elevado a B"""
    def __init__(self):
        nombre = "Pow(x,y)"
        Funcion.__init__(self, nombre)

    def __call__(self, var1, var2):
        import math
        return math.pow(float(var1), float(var2))
    

