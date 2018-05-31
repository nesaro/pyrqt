#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2008  Néstor Arocha Rodríguez

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

"""Temas para qt4"""

from PyQt4.QtGui import QPixmap

class GestorTemas:
    """
    Gestiona los temas. Su utilidad real queda pendiente 
    de futuros diseños
    """
    def __init__(self):
        import os
        self.ruta = None
        posiblesrutas = ["Driza/carga/images/", \
                "/usr/lib/python2.4/site-packages/Driza/carga/images/", \
                "~/.driza/images/"]
        for ruta in posiblesrutas:
            if os.path.exists(ruta):
                self.ruta = ruta
                break

        if not self.ruta:
            raise IOError

    def portada(self):
        """Devuelve el QPixmap con la imagen de portada"""
        return QPixmap(self.ruta + "driza.png")

    def icono_abrir(self):
        """Devuelve un QPixmap con el icono de abrir"""
        return QPixmap(self.ruta + "botonabrir.png")

    def icono_guardar(self):
        """Devuelve un QPixmap con el icono de guardar"""
        return QPixmap(self.ruta + "botonguardar.png")

    def icono_nueva_ventana(self):
        """Devuelve un QPixmap con el icono de ventana nueva"""
        return QPixmap(self.ruta + "botonnuevaventana.png")

    def icono_etiquetas(self):
        """Devuelve un QPixmap con el icono de etiqutas"""
        return QPixmap(self.ruta + "botonetiquetas.png")

    def icono_exportar(self):
        """Devuelve un QPixmap con el icono de exportar"""
        return QPixmap(self.ruta + "botonexportar.png")

    def icono_programa(self):
        """Devuelve un QPixmap con el icono miniatura del programa"""
        return QPixmap(self.ruta + "icono-driza.png")


