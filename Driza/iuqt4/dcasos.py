#!/usr/bin/python
# -*- coding: utf-8 -*-
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

from qt import *
from Driza.ui.dialogos.uidcasos import DialogoCasos

#Dialogo de casos

#textLabel1: Etiqueta donde poner el nombre de la variable
#lineEdit1:  zona donde escribes la nueva clave
#lineEdit2:  zona donde escribes el nuevo valor
#listBox1: Donde se muestra todo

#PushButton1: Boton aceptar
#PushButton2: Boton de cancelar
#pushButton3: Añadir la entrada a la lista
#pushButton4: Borrar una entrada de la lista

class DCasos(DialogoCasos):
	"""Permite, dada una variable, asignar a cada posible valor de esta una cadena de texto"""

	def __init__(self,parent,dato):
		"""Inicialización del dialogo de casos"""
		DialogoCasos.__init__(self,parent,"Dialogo casos",0,0)
		#VARIABLES PRIVADAS
		self.__variable=None
		self.__dato=dato

		self.__conexiones()
		self.listBox1.clear()
	#FUNCIONES PUBLICAS

	def mostrar(self,variable):
		self.__variable=variable
		if self.__dato.getVar(self.__variable).tipo!="Entero":
			rc = QMessageBox.warning(self,'Error', 'En esta versión solo los Enteros aceptan casos')
			self.reject()
		else:
			self.show()

	def myUpdate(self):
		self.textLabel1.setText("Variable:"+self.__dato.getVar(self.__variable).nombre)
		self.listBox1.clear()
		for pareja in self.__dato.getVar(variable).valores.items():
			self.listBox1.insertItem(str(pareja[0])+"      "+str(pareja[1]))

	def showEvent(self,ev):
		self.myUpdate()
		DialogoCasos.showEvent(self,ev)

	def accept(self):
		"""Redefinición del accept de la clase padre. Desvincula al dialogo de la variable con la que estaba trabajando"""
		self.__variable=None
		DialogoCasos.accept(self)


	#FUNCIONES PRIVADAS

	def __addclave(self):
		"""Añade una pareja clave:valor a la variable"""
		if self.__variable!=None and self.lineEdit2.text().latin1() and self.lineEdit1.text().latin1(): #Tiene que existir la variable destino, el valor y la clave
			#De momento solo trabaja con enteros como indices
			self.__dato.getVar(self.__variable).valores[self.lineEdit1.text().latin1()]=self.lineEdit2.text().latin1()
			self.show(self.__variable)
		else:
			rc = QMessageBox.warning(self,'Atencion', 'Falta el valor o clave', 'Volver al dialogo','',0)

	def __borrarclave(self):
		"""Borra la clave señalada por listBox1"""
		del self.__dato.getVar(self.__variable).valores[self.listBox1.currentText().latin1().split(" ")[0]]
		self.show(self.__variable)


	def __conexiones(self):
		"""Bloque de conexiones"""
		self.connect(self.pushButton1,SIGNAL("clicked()"),self.accept)
		self.connect(self.pushButton2,SIGNAL("clicked()"),self.reject)
		self.connect(self.pushButton3,SIGNAL("clicked()"),self.__addclave)
		self.connect(self.pushButton4,SIGNAL("clicked()"),self.__borrarclave)

