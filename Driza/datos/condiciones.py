#!/usr/bin/python
# -*- coding: utf-8 -*-
#

#Copyright (C) 2006-2007  Inmaculada Luengo Merino, Néstor Arocha Rodríguez

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

"""
Condiciones: Todas las clases relacionadas con la futura infraestructura
de querys y condiciones
"""


def procesa_condicion(datos, ristra):
    """
    Funcion que devuelve un objeto condicion a partir de una ristra que ha 
    pasado el usuario
    """
    import re
    esseleccion = re.compile(".*=.*")
    if esseleccion.match(ristra):
        lista = ristra.split("=")
        assert(len(lista)==2)
        var = datos.var(lista[0])
        elem = var.nuevo_item(lista[1])
        return Seleccion(var, elem)
    
#Abstracta
class Condicion:
    """Esta clase expresara una condicion parecida a las de tipo SQL"""
    def __init__(self):
        pass

class Seleccion(Condicion):
    """ 
    Esto es una condicion de filtrado de seleccion es equivalente 
    en SQL 'where variable=valor'
    """
    def __init__(self, variable, valor):
        assert(valor.tvariable == variable)
        self.variable = variable
        self.valor = valor

    def __call__(self, registro):
        """
        Llamando a la funcion establecemos si el registro 
        pasa la condicion de seleccion o no
        """
        return registro[self.variable] == self.valor
