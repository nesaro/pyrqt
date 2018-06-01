#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2008  Néstor Arocha Rodríguez

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

"""Dialogo de creacion de variables"""
#pushButton1: Boton aceptar
#pushButton2: Cancelar
#pushButton3: Boton de inclusion de funciones en caja de texto
#pushButton4 Inclusión de variable en caja de texto
#textEdit1: Caja de escritura
#listbox1: listado de variables
#listbox2: listado categoria funciones
#listbox3: listado funciones
#lineEdit1: Caja con el nombre de la variable
#lineEdit2: Caja con la descripción
#comboBox1: Caja con el tipo


from pyrqt.iuqt4.ui.dcrevar import Ui_DialogoCrevar
from PyQt4 import QtCore, QtGui
import logging
LOG = logging.getLogger("__name__")


class DCrevar(QtGui.QDialog):
    """Dialogo de creación de variables, permite obtener nuevas variables a partir de las ya existentes"""

    def __init__(self, parent, dato, config,gestorpaquetes):
        """Inicialización"""
        QtGui.QDialog.__init__(self, parent)
        self.ui=Ui_DialogoCrevar()
        self.ui.setupUi(self)
        #VARIABLES PRIVADAS
        self.__gestorpaquetes = gestorpaquetes
        self.__config = config
        self.__idu = dato
        self.ui.checkBox2.setDisabled(True)

        self.__init_lista_tipos()
        self.__conexiones()
    #FUNCIONES PUBLICAS        

    def showEvent(self, ev):
        """Redefinición del showevent de qt"""
        self.__actualizar_cajas()
        QtGui.QDialog.showEvent(self, ev)
    
    def accept(self):
        """Función de aceptación del dialogo. 
        Avisa al usuario si los datos han sido introducidos incorrectamente, y genera"""
        if self.ui.lineEdit1.text():
            from pyrqt.excepciones import VariableExisteException
            sobreescritura = self.ui.checkBox1.isChecked()
            solofiltrado = False
            if sobreescritura:
                if self.ui.checkBox2.isChecked():
                    solofiltrado = True
            try:
                self.__idu.ana_var_expresion(self.ui.lineEdit1.text(), self.ui.comboBox1.currentText(), \
                        "NA", self.ui.lineEdit2.text(),self.ui.textEdit1.toPlainText(), \
                        permitirsobreescritura=sobreescritura, solofiltrados=solofiltrado)
            except (SyntaxError,NameError):
                #La expresión no es correcta, mostramos un mensaje de error
                LOG.exception("Excepción al añadir la variable con la expresión")
                QErrorMessage(self, "error").message(u"La expresión no es correcta")
                self.__idu.borrar_var(self.ui.lineEdit1.text().latin1()) #Borrar la variable que está a medias
            except (ZeroDivisionError,OverflowError):
                QErrorMessage(self, "error").message(u"La expresión genera un desbordamiento")
            except VariableExisteException:
                QMessageBox.warning(self, u"atención", u"La variable ya existe")
            except TypeError:
                QErrorMessage(self, "error").message(u"El tipo de variable no coincide con el existente")
                LOG.exception("Excepción al añadir la variable con la expresión")
            else:
                QtGui.QDialog.accept(self)
                self.parent().grid.myUpdate()
        else:
            returncode = QtGui.QMessageBox.warning(self, 'Atencion', \
                    'No has rellenado todos los campos', \
                    'Volver al dialogo', 'Salir', '', 0, 1 )
            if returncode == 1:
                self.reject()


    #FUNCIONES PRIVADAS
    def __conexiones(self):
        """Bloque de conexiones"""
        from PyQt4.QtCore import SIGNAL
        self.connect(self.ui.pushButton1,SIGNAL("clicked()"), self.accept)
        self.connect(self.ui.pushButton2,SIGNAL("clicked()"), self.reject)
        self.connect(self.ui.pushButton3,SIGNAL("clicked()"), self.__insertar_funcion_seleccionada)
        self.connect(self.ui.pushButton4,SIGNAL("clicked()"), self.__insertar_variable_seleccion)
        self.connect(self.ui.comboBox1,SIGNAL("activated(int)"),self.__actualizar_cajas)
        self.connect(self.ui.listWidget_2,SIGNAL("itemSelectionChanged()"), self.__actualizar_lista_funciones)
        self.connect(self.ui.pushButton5, SIGNAL("clicked()"), self.__insertar_simbolo_mas)
        self.connect(self.ui.pushButton6, SIGNAL("clicked()"), self.__insertar_simbolo_menos)
        self.connect(self.ui.pushButton7, SIGNAL("clicked()"), self.__insertar_simbolo_asterisco)
        self.connect(self.ui.pushButton8, SIGNAL("clicked()"), self.__insertar_simbolo_barra)
        self.connect(self.ui.pushButton9, SIGNAL("clicked()"), self.__insertar_simbolo_2_asteriscos)
        self.connect(self.ui.checkBox1, SIGNAL("clicked()"), self.__activar_checkbox2)

    def __actualizar_cajas(self):
        """Actualiza todas las cajas"""
        self.__actualizar_caja_vars()
        self.__actualizar_tipo_funciones()


    def __actualizar_caja_vars(self):
        """Actualiza la caja de variables disponibles"""
        self.ui.listWidget.clear()
        j=0
        for var in self.__idu.lista_tit():
            if cmp(self.ui.comboBox1.currentText(), self.__idu.var(j).tipo)==0:
                self.ui.listWidget.addItem(var)
            j+=1
    
    def __init_lista_tipos(self):
        """Rellena en el comboBox1 la lista de tipos de variables"""
        self.ui.comboBox1.clear()
        from pyrqt.listas import SL
        for tipo in SL.nombrevariables:
            self.ui.comboBox1.addItem(tipo)

    def __actualizar_tipo_funciones(self):
        """Actualiza la lista de tipo de funciones en funcion del tipo destino"""
        self.ui.listWidget_2.clear()
        for paquete in self.__gestorpaquetes.iterkeys():
            self.ui.listWidget_2.addItem(paquete)
    
    def __insertar_variable_seleccion(self): 
        """Coge el valor seleccionado y lo añade en la caja de texto"""
        if self.ui.listWidget.currentItem() != -1:
            texto = self.ui.listWidget.currentItem().text()
            self.ui.textEdit1.insertPlainText(texto)

    def __insertar_funcion_seleccionada(self):
        """Inserta la funcion seleccionada en la caja de texto"""
        if self.ui.listWidget_3.currentItem():
            texto = self.ui.listWidget_3.currentItem().text()
            self.ui.textEdit1.insertPlainText(texto)

    def __actualizar_lista_funciones(self):
        """Actualiza la lista de funciones en función del paquete seleccionado"""
        self.ui.listWidget_3.clear()
        if cmp(self.ui.listWidget_2.currentItem().text(), u"Aritméticas") == 0:
            #Estamos con las aritmeticas
            self.ui.listWidget_3.insertItem("+")
            self.listBox3.insertItem("-")
            self.listBox3.insertItem("*")
            self.listBox3.insertItem("/")
        elif cmp(self.ui.listWidget_2.currentItem().text(), u"Lógicas") == 0:
            self.listBox3.insertItem("and")
            self.listBox3.insertItem("or")
        else:
            lista = self.__gestorpaquetes[str(self.ui.listWidget_2.currentItem().text())].values()
            for funcion in lista:
                self.ui.listWidget_3.addItem(funcion.nombre)

    def __insertar_simbolo_mas(self): 
        """Inserta el simbolo de adición"""
        self.ui.textEdit1.insertPlainText("+")
    def __insertar_simbolo_menos(self): 
        """Inserta el simbolo de sustracción"""
        self.ui.textEdit1.insertPlainText("-")
    def __insertar_simbolo_asterisco(self): 
        """Inserta el simbolo de multiplicación"""
        self.ui.textEdit1.insertPlainText("*")
    def __insertar_simbolo_barra(self): 
        """Inserta el simbolo de división"""
        self.ui.textEdit1.insertPlainText("/")
    def __insertar_simbolo_2_asteriscos(self): 
        """Inserta el simbolo de potencia"""
        self.ui.textEdit1.insertPlainText("**")

    def __activar_checkbox2(self):
        """Determina si debe estar activo el segundo checkbox, y actualiza su estado"""
        if self.ui.checkBox1.isChecked(): 
            self.ui.checkBox2.setEnabled(True)
        else: 
            self.ui.checkBox2.setDisabled(True)
