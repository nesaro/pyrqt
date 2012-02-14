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


"""Dialogo de configuracion"""

from Driza.iuqt3.ui.dconfig import DialogoConfig
from Driza.iuqt3.ui.wconfig1 import wconfig1
from qt import SIGNAL, QMessageBox

class DConfig(DialogoConfig):
    """Permite configurar cualquier aspecto del programa. Esta vinculado al objeto ManejadorConfig"""

    def __init__(self, config, parent = None,):
        DialogoConfig.__init__(self, parent, "DialogoConfig", 0, 0)
        #VARIABLES PRIVADAS
        self.__cambiado = False
        self.__config = config

        self.listBox.clear()
        self.listBox.insertItem("General")
        #Inicializacion de widgets
        self.__wgeneral = wconfig1(self.widgetStack1, "ficheros",)
        self.widgetStack1.addWidget(self.__wgeneral, 1)
        #Seleccionar por defecto el valor 0 y poblarlo
        self.__mostrar_caja(1)
        self.__conexiones()

    #FUNCIONES PUBLICAS
    def accept(self):
        """Funcion redefinida que establece que debe hacer el dialogo cuando el usuario pulsa aceptar.
        Ante un cambio en los campos del dialogo, pregunta al usuario si guarda la configuración
        """
        if not self.__cambiado:
            DialogoConfig.accept(self)
        else:
            self.__cambiado = False # Volvemos a ponerlo en falso
            codigoretorno = QMessageBox.information(self, u'Atención: Guardar', \
                    u'Ha cambiado la configuración, desea guardarla?', \
                    'Guardarla', 'Cancelar', 'Dejarlo estar', 0, 1)
            if codigoretorno == 0:
                #Crear una interfaz usuario configuracion #DECISION DE DISEÑO, pendiente
                self.__guardar_config()
                DialogoConfig.accept(self)
            elif codigoretorno == 2:
                DialogoConfig.reject(self)
            else:
                self.__cambiado = True

    
    #FUNCIONES PRIVADAS

    def __mostrar_caja(self, numero): # El numero es el indice de la listBox
        """Puebla la caja donde se encuentra la seccion"""
        if numero == 1:
            self.widgetStack1.raiseWidget(1)
            self.__wgeneral.lineEdit1.setText(self.__config.configuracion["tmpdir"])
            self.__wgeneral.checkBox1.setChecked(self.__config.configuracion["vsplash"])
            self.__wgeneral.spinBox1.setValue(self.__config.configuracion["decimales"])
            self.__wgeneral.spinBox2.setValue(self.__config.configuracion["nundo"])

    def __conexiones(self):
        """Bloque de conexiones"""
        self.connect(self.__wgeneral.lineEdit1, SIGNAL("textChanged(const QString&)"), self.__cambio)
        self.connect(self.__wgeneral.checkBox1, SIGNAL("clicked()"), self.__cambio)
        self.connect(self.__wgeneral.spinBox1, SIGNAL("valueChanged(int)"), self.__cambio)
        self.connect(self.__wgeneral.spinBox2, SIGNAL("valueChanged(int)"), self.__cambio)

    def __cambio(self):
        """Almacena si se ha producido algun cambio"""
        self.__cambiado = True

    def __guardar_config(self):
        """Guarda la configuración en el objeto que la maneja"""
        self.__config.configuracion["tmpdir"] = str(self.__wgeneral.lineEdit1.text())
        self.__config.configuracion["vsplash"] = self.__wgeneral.checkBox1.isChecked()
        self.__config.configuracion["decimales"] = int(self.__wgeneral.spinBox1.value())
        self.__config.configuracion["nundo"] = int(self.__wgeneral.spinBox2.value())
        self.__config.guardar()
