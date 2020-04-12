#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007  Néstor Arocha Rodriguez, Inmaculada Luengo Merino

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

"""Definicion de las clases que representan variables"""

import logging
LOG = logging.getLogger(__name__)

def isnan(x):
    return isinstance(x, float) and x != x

class Variable:
    """La clase padre de todas las variables"""
    def __init__(self, agrupador, valor):
        self.tvariable = agrupador
        if isinstance(valor, self.__class__):
            self.valor = getattr(valor, 'valor')
        self.valor = self._interno(valor) #pylint: disable=no-member

    def valido(self):
        """Devuelve verdadero si el valor es valido"""
        return self.valor != None

    def __cmp__(self, otro):
        if self.valor is None:
            return False
        if isinstance(otro, Variable):
            if otro.valor is None:
                return False
            else:
                return self.valor.__cmp__(otro.valor)
        else:
            return self.valor.__cmp__(otro) #Delegamos la excepcion a la clase de otro

    def __str__(self):
        if not self.valido():
            return ""
        return str(self.valor)

class VariableNumerica(Variable):
    """Las clases que heredan son numericas. Esta clase solo aporta esa informacion de momento"""
    def __add__(self, otro):
        if self.valor is None:
            return None
        return self.valor + int(float(otro))

    def __eq__(self, otro):
        if isinstance(otro, VariableNumerica):
            return self.valor == otro.valor
        if self.valor is None or otro is None:
            return False
        return self.valor == float(otro)

    def __pow__(self, exponente):
        if self.valido():
            if isinstance(exponente, VariableNumerica):
                return self.valor.__pow__(exponente.valor)
            return self.valor.__pow__(exponente)
        return float('nan')

    def __rpow__(self, base):
        if self.valido():
            if isinstance(base, VariableNumerica):
                return self.valor.__rpow__(base.valor)
            return self.valor.__rpow__(base)
        return float('nan')


class VariableDiscreta(Variable):
    """Clase que representa a las variables discretas. Permiten la comparacion directa entre valores"""
    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.valor == other.valor
        return self.valor == other

class Entero(VariableDiscreta, VariableNumerica):
    """Toda variable que tiene como representacion interna un entero"""
    def _interno(self, valor):
        """Actua como constructor, devolviendo el valor que almacena la variable"""
        if valor is None or valor == "None" or valor == "NA"\
                or valor == "nan" or valor == float("nan") or valor == "":
            return None
        if isinstance(valor, str):
            resultado = int(valor)
        elif isinstance(valor, int) or isinstance(valor, long) or isinstance(valor, float):
            resultado = int(valor)
        elif isinstance(valor, self.__class__):
            resultado = valor.valor
        else:
            LOG.debug("Entero._interno: No se pudo convertir el valor pasado de tipo "+str(valor.__class__))
            raise TypeError
        if isinstance(resultado, long):
            resultado = int(resultado)
        return resultado

    def to_R(self):
        """Convert value to R format"""
        return self.__float__()

    def __float__(self):
        if not self.valido():
            raise ValueError
        return float(self.valor)

    def __int__(self):
        if not self.valido():
            raise ValueError
        return int(self.valor)

    def etiqueta(self):
        """Devuelve la etiqueta del valor en caso de que exista"""
        if self.valido():
            if str(self.valor) in self.tvariable.etiquetas:
                return self.tvariable.etiquetas[str(self.valor)]
        return self.__str__()

    def __cmp__(self, otro):
        if isinstance(otro, float) or isinstance(otro, long) or isinstance(otro, int):
            return int(self.valor).__cmp__(int(otro))
        return Variable.__cmp__(self, otro)

class Factor(VariableDiscreta):
    """Las variables que solo son cadenas y que unicamente sirven para agrupacion"""
    def _interno(self, cadena):
        """Actua como constructor, devolviendo el valor que almacena la variable"""
        if cadena == "''":
            return str()
        if isinstance(cadena, str):
            return cadena
        return str(cadena)

    def to_R(self):
        """Convert value to R format"""
        raise ValueError

    def __str__(self):
        if self.valido():
            return self.valor
        return ''

    def __cmp__(self, otrovalor):
        if self.valor is None:
            return False
        if isinstance(otrovalor, Variable):
            if otrovalor.valor is None:
                return False
            else:
                return self.__compare(otrovalor.valor)
        else:
            return self.__compare(otrovalor) #Delegamos la excepcion a la clase de otro

    def __compare(self, otrovalor):
        """Comparacion de cadenas, asiste a __cmp__"""
        if self.valor < otrovalor: 
            return -1
        elif self.valor > otrovalor: 
            return 1
        else: 
            return 0


class Real(VariableNumerica):
    """Variables de coma flotante"""
    def _interno(self, valor):
        """Actua como constructor, devolviendo el valor que almacena la variable"""
        if isinstance(valor, Real):
            return valor.valor
        if valor is None or valor == "None" or valor == "NA"\
                or valor == "nan" or isnan(valor)\
                or valor == "":
            return None
        return float(valor)

    def to_R(self):
        """Convert value to R format"""
        return self.__float__()

    def __float__(self):
        if not self.valido():
            raise ValueError
        return self.valor

    def __cmp__(self, otrovalor):
        if self.valor is None:
            return False
        if isinstance(otrovalor, Variable):
            if otrovalor.valor is None:
                return False
            else:
                return self.__compare(otrovalor.valor)
        else:
            return self.__compare(otrovalor) #Delegamos la excepcion a float

    def __compare(self, valor):
        """Hace el equivalente de comparacion para el float"""
        if self.valor > valor:
            return 1
        elif self.valor < valor:
            return -1
        else: return 0

    def __str__(self):
        if not self.valido():
            return ""
        #ristra ="%8."+str(self.tvariable.numerodecimales) +"g"
        if str(self.valor).find(".")!=-1:
            decimales = str(self.valor).split(".")[1]
            if len(str(decimales)) > self.tvariable.numerodecimales:
                ristra ="%8." + str(self.tvariable.numerodecimales) + "f"
                return ristra % self.valor
        return str(self.valor)



class Logico(VariableDiscreta):
    """Tipo logico (booleano"""
    def _interno(self, valor):
        """Actua como constructor, devolviendo el valor que almacena la variable"""
        if valor is None or valor == "None" or valor == "NA"\
                or valor == "nan" or valor == float("nan") or valor == "":
            return None
        elif valor == True or valor == "True"\
                or valor == "Verdadero" or valor == "1":
            return True
        else:
            return False

    def __nonzero__(self):
        if self.valor is None: 
            return False
        return self.valor.__nonzero__()

    def __eq__(self, otro):
        if self.valor is None:
            return False
        if isinstance(otro, Logico):
            return otro.valor == self.valor
        if otro == True or otro == False:
            return otro == self.valor


    def __xor__(self, otro):
        if self.valor is None:
            return False
        return self.valor.__xor__(otro.valor)

    def __int__(self):
        if self.valor is None:
            return None
        return int(self.valor)

    def __cmp__(self, otro):
        if self.valor is None:
            return False
        return self.valor.__cmp__(otro.valor)

    def __str__(self):
        if self.valor is None: 
            return ""
        elif self.valor == True:
            return "1"
        elif self.valor == False: 
            return "0"

    def to_R(self):
        """Convert value to R format"""
        raise ValueError
