#!/usr/bin/python

# Copyright (C) 2006-2008  Néstor Arocha Rodríguez

# This file is part of Driza.
#
# Driza is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Driza is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Driza; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""Dialogo de configuracion"""

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QDialog
from .ui.dconfig import Ui_DialogoConfig
from .ui.wconfig1 import Ui_wconfig1


class DConfig(QDialog):
    """Permite configurar cualquier aspecto del programa. Esta vinculado al objeto ManejadorConfig"""

    def __init__(
        self,
        config,
        parent=None,
    ):
        super().__init__(parent)
        self.ui = Ui_DialogoConfig()
        self.ui.setupUi(self)
        self.__wgeneral = QDialog()
        self.__wgeneralui = Ui_wconfig1()
        self.__wgeneralui.setupUi(self.__wgeneral)
        # VARIABLES PRIVADAS

        self.__cambiado = False
        self.__config = config

        self.ui.listWidget.clear()
        self.ui.listWidget.insertItem(0, str("General"))
        # Inicializacion de widgets
        # self.__wgeneral=wconfig1(self.widgetStack1,"ficheros",)
        self.ui.stackedWidget.addWidget(self.__wgeneral)
        # Seleccionar por defecto el valor 0 y poblarlo
        self.__mostrar_caja(1)
        self.__conexiones()

    # FUNCIONES PUBLICAS
    def accept(self):
        """Funcion redefinida que establece que debe hacer el dialogo cuando el usuario pulsa aceptar.
        Ante un cambio en los campos del dialogo, pregunta al usuario si guarda la configuración
        """
        if not self.__cambiado:
            super().accept()
            return
        return_value = QMessageBox.question(
            self,
            "Atención: Guardar",
            "Ha cambiado la configuración, desea guardarla?",
            buttons=QMessageBox.Save | QMessageBox.Cancel | QMessageBox.Discard,
        )
        if return_value == QMessageBox.Save:
            # Crear una interfaz usuario configuracion #DECISION DE DISEÑO, pendiente
            self.__guardar_config()
            self.__cambiado = False  # Volvemos a ponerlo en falso
            super().accept()
        elif return_value == QMessageBox.Cancel:
            self.__cambiado = False  # Volvemos a ponerlo en falso
            super().reject()

    # FUNCIONES PRIVADAS

    def __mostrar_caja(self, numero: int):  # El numero es el indice de la listBox
        """Puebla la caja donde se encuentra la seccion"""
        if numero == 1:
            self.ui.stackedWidget.setCurrentWidget(self.__wgeneral)
            self.__wgeneralui.lineEdit1.setText(self.__config.configuracion["tmpdir"])
            self.__wgeneralui.checkBox1.setChecked(
                self.__config.configuracion["vsplash"]
            )
            self.__wgeneralui.spinBox1.setValue(
                self.__config.configuracion["decimales"]
            )
            self.__wgeneralui.spinBox2.setValue(self.__config.configuracion["nundo"])

    def __conexiones(self):
        """Bloque de conexiones"""
        self.__wgeneralui.lineEdit1.textChanged.connect(self.__cambio)
        self.__wgeneralui.checkBox1.clicked.connect(self.__cambio)
        self.__wgeneralui.spinBox1.valueChanged.connect(self.__cambio)
        self.__wgeneralui.spinBox2.valueChanged.connect(self.__cambio)

    def __cambio(self):
        """Almacena si se ha producido algun cambio"""
        self.__cambiado = True

    def __guardar_config(self):
        """Guarda la configuración en el objeto que la maneja"""
        self.__config.configuracion["tmpdir"] = str(self.__wgeneralui.lineEdit1.text())
        self.__config.configuracion["vsplash"] = self.__wgeneralui.checkBox1.isChecked()
        self.__config.configuracion["decimales"] = int(
            self.__wgeneralui.spinBox1.value()
        )
        self.__config.configuracion["nundo"] = int(self.__wgeneralui.spinBox2.value())
        self.__config.save()
