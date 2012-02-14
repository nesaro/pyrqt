#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007  Néstor Arocha Rodríguez

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

"""Dialogo de filtrado"""


from PyQt4 import QtCore,QtGui
from Driza.iuqt4.ui.dfiltrado import Ui_DialogoFiltro
import logging
log = logging.getLogger("Driza.iuqt4.ui.dfiltrado")


class DFiltrado(QtGui.QDialog):
    """Dialogo que permite establecer el filtro"""
    
    def __init__(self,parent,interfazdatosusuario):
        QtGui.QDialog.__init__(self, parent)
        self.ui=Ui_DialogoFiltro()
        self.ui.setupUi(self)
        self.__conexiones()
        self.__idu = interfazdatosusuario

    def __conexiones(self):
        """Función que define las conexiones entre elementos de la interfaz y sus SLOTS"""
        from PyQt4.QtCore import SIGNAL
        self.connect(self.ui.pushButton1,SIGNAL("clicked()"),self.accept)
        self.connect(self.ui.pushButton2,SIGNAL("clicked()"),self.reject)
        self.connect(self.ui.pushButton3,SIGNAL("clicked()"),self.__insertarSimboloGT)
        self.connect(self.ui.pushButton4,SIGNAL("clicked()"),self.__insertarSimboloLT)
        self.connect(self.ui.pushButton5,SIGNAL("clicked()"),self.__insertarSimboloEQ)
        self.connect(self.ui.pushButton6,SIGNAL("clicked()"),self.__insertarSimboloNE)
        self.connect(self.ui.pushButton7,SIGNAL("clicked()"),self.__insertar_simbolo_AND)
        self.connect(self.ui.pushButton8, SIGNAL("clicked()"), self.__insertar_simbolo_OR)
        self.connect(self.ui.pushButton9, SIGNAL("clicked()"), self.__desactivarfiltro)
        self.connect(self.ui.pushButton10, SIGNAL("clicked()"), self.__insertar_simbolo_XOR)
        self.connect(self.ui.pushButton11, SIGNAL("clicked()"), self.__insertar_simbolo_LE)
        self.connect(self.ui.pushButton12, SIGNAL("clicked()"), self.__insertar_simbolo_GE)
        self.connect(self.ui.comboBox1,SIGNAL("activated (int)"),self.__insertarvariable)

    def showEvent(self,ev):
        """Redefinicion de showEvent de qt"""
        self.myUpdate()
        QtGui.QDialog.showEvent(self,ev)

    def accept(self):
        """Aceptación del dialogo"""
        expresion = self.ui.textEdit.toPlainText()
        if not expresion:#Si no se rellena nada, se desactiva el filtro
            self.__desactivarfiltro()
        else:
            try:
                self.__idu.establecer_filtro(expresion)
            except SyntaxError:
                log.exception("Capturada excepcion en el manejo del filtro")
            else:
                self.parent().grid.myUpdate()
                QtGui.QDialog.accept(self)


    def __insertarSimboloGT(self):
        self.ui.textEdit.insertPlainText(">")
    def __insertarSimboloLT(self):
        self.ui.textEdit.insertPlainText("<")
    def __insertarSimboloEQ(self):
        self.ui.textEdit.insertPlainText("==")
    def __insertarSimboloNE(self):
        self.ui.textEdit.insertPlainText("!=")

    def __insertar_simbolo_AND(self): 
        """Inserta el simbolo "y" (lógico) """
        self.ui.textEdit.insert(" and ")
    def __insertar_simbolo_OR(self): 
        """Inserta el simbolo "o" (lógico) """
        self.ui.textEdit.insert(" or ")
    def __insertar_simbolo_XOR(self): 
        """Inserta el simbolo "o extendido" (lógico) """
        self.ui.textEdit.insert("^")
    def __insertar_simbolo_GE(self): 
        """Inserta el simbolo "mayor o igual" """
        self.ui.textEdit.insert(">=")
    def __insertar_simbolo_LE(self): 
        """Inserta el simbolo "menor o igual" """
        self.ui.textEdit.insert("<=")


    def __insertarvariable(self,indice=0):
        """Inserta la variable seleccionada en el comboBox1"""
        self.ui.textEdit.insertPlainText(self.ui.comboBox1.currentText())

    def __desactivarfiltro(self):
        """Desactiva el filtro"""
        self.__idu.delFiltro() 
        self.parent().grid.myUpdate()
        QtGui.QDialog.accept(self)


    def __actualizarcombovars(self):
        """Actualiza la caja de variables disponibles"""
        self.ui.comboBox1.clear()
        for var in self.__idu.lista_tit():
            self.ui.comboBox1.addItem(QtCore.QString(var))

    def myUpdate(self):
        """Actualizacion del dialogo"""
        self.__actualizarcombovars()


