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

"""Dialogo de casos"""

from qt import QMessageBox, SIGNAL
from Driza.iuqt3.ui.dcasos import DialogoCasos


class DCasos(DialogoCasos):
    """Permite, dada una variable, asignar a cada posible valor de esta 
    una cadena de texto"""

    def __init__(self, parent, dato):
        """Inicialización del dialogo de casos"""
        DialogoCasos.__init__(self, parent, "Dialogo casos", 0, 0)
        #VARIABLES PRIVADAS
        self.__variable = None
        self.__idu = dato

        self.__conexiones()
        self.listBox1.clear()
    #FUNCIONES PUBLICAS

    def mostrar(self, variable = None):
        """Funcion sustituta de show que permite 
        escoger la variable a mostrar"""
        if variable != None:
            self.__variable = variable
        if not "etiquetable" in self.__idu.var(self.__variable).tags:
            QMessageBox.warning(self, 'Error', \
                    'Solo los Enteros y Ordinales aceptan casos')
            self.reject()
        else:
            self.raiseW()
            self.show()

    def __myUpdate(self):
        """Funcion de actualizacion del dialogo. Es llamado desde showEvent"""
        self.textLabel1.setText("Variable:" + \
                self.__idu.var(self.__variable).name())
        self.listBox1.clear()
        for pareja in self.__idu.var(self.__variable).etiquetas.items():
            self.listBox1.insertItem(str(pareja[0]) + "      " + str(pareja[1]))

    def showEvent(self, event):
        """Redefinición función qt"""
        self.__myUpdate()
        DialogoCasos.showEvent(self, event)

    def accept(self):
        """Redefinición del accept de la clase padre. 
        Desvincula al dialogo de la variable con la que estaba trabajando"""
        self.__variable = None
        DialogoCasos.accept(self)


    #FUNCIONES PRIVADAS

    def __anadir_clave(self):
        """Añade una pareja clave:valor a la variable"""
        #Tiene que existir la variable destino, el valor y la clave
        if self.__variable != None and self.lineEdit2.text().latin1() \
                and self.lineEdit1.text().latin1():            
            #De momento solo trabaja con enteros como indices
            self.__idu.var(self.__variable).\
                    etiquetas[self.lineEdit1.text().latin1()] = \
                    self.lineEdit2.text().latin1()
            self.__myUpdate()
        else:
            QMessageBox.warning(self, 'Atencion', 
                    'Falta el valor o clave', 'Volver al dialogo', '', 0)

    def __borrar_clave(self):
        """Borra la clave señalada por listBox1"""
        entrada = self.listBox1.currentText().latin1().split(" ")[0]
        del self.__idu.var(self.__variable).etiquetas[entrada]
        self.__myUpdate()


    def __conexiones(self):
        """Bloque de conexiones"""
        self.connect(self.pushButton1, SIGNAL("clicked()"), self.accept)
        self.connect(self.pushButton2, SIGNAL("clicked()"), self.reject)
        self.connect(self.pushButton3, SIGNAL("clicked()"), self.__anadir_clave)
        self.connect(self.pushButton4, SIGNAL("clicked()"), self.__borrar_clave)

