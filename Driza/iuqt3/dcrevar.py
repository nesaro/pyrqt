#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007  Néstor Arocha Rodríguez,Inmaculada Luengo Merino 

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

"""Dialogo de creacion de variables"""

from Driza.iuqt3.ui.dcrevar import DialogoCrevar
from qt import SIGNAL, QErrorMessage, QMessageBox
import logging
LOG = logging.getLogger("Driza.iuqt3.dcrevar")


class DCrevar(DialogoCrevar):
    """Dialogo de creación de variables, permite obtener nuevas variables a partir de las ya existentes"""

    def __init__(self, parent, dato, config, gestorpaquetes):
        """Inicialización"""
        DialogoCrevar.__init__(self, parent, "dialogo Creacion variables", 0, 0)
        #VARIABLES PRIVADAS
        self.__gestorpaquetes = gestorpaquetes
        self.__config = config
        self.__idu = dato 
        self.checkBox2.setDisabled(True)

        self.__init_lista_tipos()
        self.__conexiones()
    #FUNCIONES PUBLICAS        

    def showEvent(self, event):
        """Redefinición del showevent de qt"""
        self.__actualizar_cajas()
        DialogoCrevar.showEvent(self, event)
    
    def accept(self):
        """Función de aceptación del dialogo. 
        Avisa al usuario si los datos han sido introducidos incorrectamente, y genera"""
        if self.lineEdit1.text():
            from Driza.excepciones import VariableExisteException
            sobreescritura = self.checkBox1.isChecked()
            solofiltrado = False
            if sobreescritura:
                if self.checkBox2.isChecked():
                    solofiltrado = True
            try:
                self.__idu.ana_var_expresion(self.lineEdit1.text().latin1(), self.comboBox1.currentText().latin1(), \
                        "NA", self.lineEdit2.text(),self.textEdit1.text().latin1(), \
                        permitirsobreescritura=sobreescritura, solofiltrados=solofiltrado)
            except (SyntaxError,NameError):
                #La expresión no es correcta, mostramos un mensaje de error
                LOG.exception("Excepción al añadir la variable con la expresión")
                QErrorMessage(self, "error").message(u"La expresión no es correcta")
                self.__idu.borrar_var(self.lineEdit1.text().latin1()) #Borrar la variable que está a medias
            except (ZeroDivisionError,OverflowError):
                QErrorMessage(self, "error").message(u"La expresión genera un desbordamiento")
            except VariableExisteException:
                QMessageBox.warning(self, u"atención", u"La variable ya existe")
            except TypeError:
                QErrorMessage(self, "error").message(u"El tipo de variable no coincide con el existente")
                LOG.exception("Excepción al añadir la variable con la expresión")
            else:
                DialogoCrevar.accept(self)
                self.parent().grid.myUpdate()
        else:
            returncode = QMessageBox.warning(self, 'Atencion', \
                    'No has rellenado todos los campos', \
                    'Volver al dialogo', 'Salir', '', 0, 1 )
            if returncode == 1:
                self.reject()


    #FUNCIONES PRIVADAS
    def __conexiones(self):
        """Bloque de conexiones"""
        self.connect(self.pushButton1, SIGNAL("clicked()"), self.accept)
        self.connect(self.pushButton2, SIGNAL("clicked()"), self.reject)
        self.connect(self.pushButton3, SIGNAL("clicked()"), self.__insertar_funcion_seleccionada)
        self.connect(self.pushButton4, SIGNAL("clicked()"), self.__insertar_variable_seleccion)
        self.connect(self.comboBox1, SIGNAL("activated(int)"), self.__actualizar_cajas)
        self.connect(self.listBox2, SIGNAL("selectionChanged()"), self.__actualizar_lista_funciones)
        self.connect(self.pushButton5, SIGNAL("clicked()"), self.__insertar_simbolo_mas)
        self.connect(self.pushButton6, SIGNAL("clicked()"), self.__insertar_simbolo_menos)
        self.connect(self.pushButton7, SIGNAL("clicked()"), self.__insertar_simbolo_asterisco)
        self.connect(self.pushButton8, SIGNAL("clicked()"), self.__insertar_simbolo_barra)
        self.connect(self.pushButton9, SIGNAL("clicked()"), self.__insertar_simbolo_2_asteriscos)
        self.connect(self.checkBox1, SIGNAL("clicked()"), self.__activar_checkbox2)

    def __actualizar_cajas(self):
        """Actualiza todas las cajas"""
        self.__actualizar_caja_vars()
        self.__actualizar_tipo_funciones()


    def __actualizar_caja_vars(self):
        """Actualiza la caja de variables disponibles"""
        self.listBox1.clear()
        i = 0
        j = 0
        for var in self.__idu.lista_tit():
            if cmp(self.comboBox1.currentText().latin1(), self.__idu.var(j).tipo) == 0:
                self.listBox1.insertItem(var, i)
                i += 1
            j += 1
    
    def __init_lista_tipos(self):
        """Rellena en el comboBox1 la lista de tipos de variables"""
        self.comboBox1.clear()
        from Driza import listas
        for tipo in listas.nombrevariables():
            self.comboBox1.insertItem(tipo)

    def __actualizar_tipo_funciones(self):
        """Actualiza la lista de tipo de funciones en funcion del tipo destino"""
        self.listBox2.clear()
        for paquete in self.__gestorpaquetes.iterkeys():
            self.listBox2.insertItem(paquete)
    
    def __insertar_variable_seleccion(self): 
        """Coge el valor seleccionado y lo añade en la caja de texto"""
        if self.listBox1.currentItem() != -1:
            texto = self.listBox1.currentText().latin1()
            self.textEdit1.insert(texto)

    def __insertar_funcion_seleccionada(self):
        """Inserta la funcion seleccionada en la caja de texto"""
        if self.listBox3.currentItem() != -1:
            texto = self.listBox3.currentText().latin1()
            self.textEdit1.insert(texto)

    def __actualizar_lista_funciones(self):
        """Actualiza la lista de funciones en función del paquete seleccionado"""
        self.listBox3.clear()
        if cmp(self.listBox2.currentText(), u"Aritméticas") == 0:
            #Estamos con las aritmeticas
            self.listBox3.insertItem("+")
            self.listBox3.insertItem("-")
            self.listBox3.insertItem("*")
            self.listBox3.insertItem("/")
        elif cmp(self.listBox2.currentText(), u"Lógicas") == 0:
            self.listBox3.insertItem("and")
            self.listBox3.insertItem("or")
        else:
            lista = self.__gestorpaquetes[unicode(self.listBox2.currentText().latin1(),'iso-8859-1')].values()
            for funcion in lista:
                self.listBox3.insertItem(funcion.nombre)

    def __insertar_simbolo_mas(self): 
        """Inserta el simbolo de adición"""
        self.textEdit1.insert("+")
    def __insertar_simbolo_menos(self): 
        """Inserta el simbolo de sustracción"""
        self.textEdit1.insert("-")
    def __insertar_simbolo_asterisco(self): 
        """Inserta el simbolo de multiplicación"""
        self.textEdit1.insert("*")
    def __insertar_simbolo_barra(self): 
        """Inserta el simbolo de división"""
        self.textEdit1.insert("/")
    def __insertar_simbolo_2_asteriscos(self): 
        """Inserta el simbolo de potencia"""
        self.textEdit1.insert("**")

    def __activar_checkbox2(self):
        """Determina si debe estar activo el segundo checkbox, y actualiza su estado"""
        if self.checkBox1.isChecked(): 
            self.checkBox2.setEnabled(True)
        else: 
            self.checkBox2.setDisabled(True)
