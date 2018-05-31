#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2008 Néstor Arocha Rodríguez

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

"""Dialogo de importacion de texto"""

from pyrqt.iuqt4.ui.dimportartexto import Ui_DialogoImportarTexto
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL


class DImportarTexto(QtGui.QDialog):
    """
    Dialogo de creación de variables, 
    permite obtener nuevas variables a partir de las ya existentes
    """

    def __init__(self, parent, interfazdatosfichero):
        QtGui.QDialog.__init__(self, parent)
                               
        self.ui = Ui_DialogoImportarTexto()
        self.ui.setupUi(self)
        self.archivo = None
        self.__idf = interfazdatosfichero
        self.__conexiones()

    def accept(self):
        """Aceptacion del dialogo"""
        if self.ui.comboBox1.currentText() == "Espacio":
            delatr = ""
        elif self.ui.comboBox1.currentText() == "Dos puntos":
            delatr = ":"
        else:
            delatr = "\t"
        cabecera = self.ui.checkBox1.isChecked()
        from rpy import RException
        try:
            self.__idf.borrar_todo()
            self.__idf.cargar_texto(self.archivo,
                                    delimitadoratrib=delatr,
                                    cabeceras=cabecera)
        except RException:
            msg = u"R No pudo importar el fichero"
            QtGui.QMessageBox.critical(self, u'Error!', msg)
            LOG.exception("Excepcion en la importacion de texto")
        QtGui.QDialog.accept(self)
        self.parent().grid.myUpdate()


    def __conexiones(self):
        """Bloque de conexiones"""
        self.connect(self.ui.pushButton1,
                     SIGNAL("clicked()"),
                     self.__seleccionar_fichero)

    def __seleccionar_fichero(self):
        """
        Detemina que hacer cuando se pulsa 
        el boton de seleccion de fichero
        """
        filtro = "%s files (*.%s);;" % ("Txt", "txt")
        cadenaarchivo = str(QtGui.QFileDialog.getOpenFileName(None,
                                                              "importar fichero",
                                                              filtro,
                                                              ""))
        if cadenaarchivo:
            self.archivo = cadenaarchivo
            self.ui.textLabel1.setText(cadenaarchivo)
