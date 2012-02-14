#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007  Néstor Arocha Rodríguez, Inmaculada Luengo Merino 

#This file is part of Driza.
#
#Driza is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by

#
#Driza is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Driza; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""Componentes de los resultados en ventana salida"""

class ComponenteSalida:
    """Cualquier elemento que figure en un resultado será hijo de esta clase"""
    def __init__(self):
        self.contenido = None
        self.titulo = ""

    def html(self):
        """Abstracta: muestra el contenido del widget volcado a html"""
        return ""

    def exportar_html(self, fichero):
        """Esta funcion es llamada cuando se desea exportar html a un fichero. 
        Normalmente hace lo mismo que html()"""
        return self.html()

    def establecer_titulo(self, titulo):
        """Establece el valor del titulo"""
        if not isinstance(titulo, str):
            raise TypeError
        self.titulo = titulo

class Tabla:
    """Clase base de las tablas. Almacena una tabla. 
    Esta clase asegura que se cumple la restriccion 
    del tamaño para todos los registros"""
    def __init__(self, autoencoger = False, decimales = 3):
        self._contenido = list()
        self._ncols = None
        self._listatitulos = []
        self._decimales = decimales
        self.autoencoger = autoencoger

    def establecer_cabecera(self, args):
        """Establece el valor de las cabeceras"""
        self._listatitulos = args

    def append(self, args):
        """Introduce los argumentos en la tabla. 
        Ha de coincidir en tamaño con ncols.Recibe ristras"""
        if not self._ncols:
            self._ncols = len(args)
        if len(args) != self._ncols:
            raise IndexError
        else:
            self._contenido.append(args)


    def _numero_validos(self):
        """Devuelve el número de elementos válidos"""
        i = 0
        for elemento in self._lista_validos():
            if elemento:
                i += 1
        return i

    def _lista_validos(self):
        """Devuelve una lista con verdaderos y falsos que determinan 
        si en esa posicion hay algún valor válido o no"""
        listafinal = []
        for i in range(len(self._listatitulos)):
            if self.autoencoger:
                vale = False
                for fila in self._contenido:
                    if fila[i] != None:
                        vale = True
            else:
                vale = True
            listafinal.append(vale)
        return listafinal

    def _tratar_elemento(self, elemento):
        """Trata un elemento devolviendo su ristra"""
        if isinstance(elemento, float):
            if str(elemento).find(".")!=-1:
                decimales = str(elemento).split(".")[1]
                if len(str(decimales)) > self._decimales:
                    ristra ="%8." + str(self._decimales) + "f"
                    salida = ristra % elemento
                else:
                    salida = str(elemento)
            else:
                salida = str(elemento)
        elif isinstance(elemento, list) or isinstance(elemento, dict) or \
                isinstance(elemento, int):
            salida = str(elemento)
        elif isinstance(elemento, str):
            salida = elemento
        else:
            raise NameError #TODO Otra excepcion
        return salida

    def html(self):
        """Devuelve el html. Llama a la función de generación de contenido
        de las clases hijos"""
        listafinal = []
        listafinal.extend(self._generar_contenido())
        cadena = u""
        for fila in listafinal:
            cadena += "<tr>\n"
            for columna in fila:
                cadena += "<td>" + columna + "</td>\n"
            cadena += "</tr>\n"
        return cadena

    def _generar_contenido(self):
        """Genera una lista con el contenido.
        Implementada por los hijos"""
        pass

class TablaHorizontal(Tabla):
    """Tabla que muestra los resultados en disposicion horizontal"""
    def _generar_contenido(self):
        """Devuelve el contenido de la tabla en html"""
        listavalidos = self._lista_validos()
        listatmp = []
        if self._listatitulos:
            i = 0
            listatmp.append([])
            for titulo in self._listatitulos:
                if listavalidos[i]:
                    listatmp[0].append(titulo)
                i += 1
        i = 0
        for fila in self._contenido:
            listatmp.append([])
            j = 0
            for campo in fila:
                if listavalidos[j]:
                    ristra = self._tratar_elemento(campo)
                    listatmp[i+1].append(ristra)
                j += 1
            i += 1
        return listatmp

class TablaVertical(Tabla):
    """Tabla que muestra los resultados en disposicion vertical"""
    def _generar_contenido(self):
        """Devuelve el contenido de la tabla una lista de listas"""
        listavalidos = self._lista_validos()
        listatmp = []
        if self._listatitulos:
            i = 0
            for titulo in self._listatitulos:
                if listavalidos[i]:
                    listatmp.append([titulo])
                i += 1
        for fila in self._contenido:
            i = 0
            j = 0
            for campo in fila:
                if listavalidos[i]:
                    ristra = self._tratar_elemento(campo)
                    listatmp[j].append(ristra)
                    j += 1 
                i += 1
        return listatmp


class CSLista(ComponenteSalida, list):
    """Varios resultados agrupados"""
    def html(self):
        """Devuelve la representación del objeto en html"""
        ristra = ""
        for componente in self:
            ristra += componente.html()
        return ristra

class CSTabla(ComponenteSalida):
    """Una tabla"""
    def __init__(self, autoencoger = False, disposicion = "Horizontal", decimales = 3):
        ComponenteSalida.__init__(self)
        if disposicion == "Horizontal":
            self.contenido = TablaHorizontal(autoencoger, decimales)
        elif disposicion == "Vertical":
            self.contenido = TablaVertical(autoencoger, decimales)
        else:
            self.contenido = TablaHorizontal(autoencoger, decimales)
            raise ValueError

    def html(self):
        """Devuelve la representación del objeto en html"""
        ristra = ""
        ristra += "<h2>" + self.titulo + "</h2>"
        ristra += "<table border=\"1\">"
        ristra += self.contenido.html()
        ristra += "</table>"
        return ristra

    def append(self, listaargs):
        """Debe recibir ristras"""
        self.contenido.append(listaargs)

    def establecer_cabecera(self, titulo):
        """Establece el valor de las cabeceras"""
        self.contenido.establecer_cabecera(titulo)

class CSTexto(ComponenteSalida):
    """Es un texto cualquiera"""
    def __init__(self, **args):
        ComponenteSalida.__init__(self)
        self.contenido = ""
        self.size = None
        if args.has_key("size"):
            self.size = args["size"]

    def establecer(self, texto):
        """Establece el valor del texto"""
        if isinstance(texto, str):
            self.contenido = texto
        elif isinstance(texto, unicode):
            self.contenido = texto.encode('iso-8859-1', 'replace')
        else:
            self.contenido(str(texto))

    def html(self):
        """Devuelve la representación del objeto en html"""
        if self.contenido:
            if self.size:
                ristra = "<font size=+" + str(self.size) + ">" + self.contenido + "</font><br>"
            else:
                ristra = self.contenido + "<br>"
            return unicode(ristra, 'iso-8859-1')
        else: 
            return u""

class CSImagen(ComponenteSalida):
    """Representa una imagen"""
    def __init__(self):
        ComponenteSalida.__init__(self)
        self.contenido = None #TODO
        self.ruta = None

    def establecer_ruta(self, ruta):
        """Establece la ruta donde se guarda la imagen"""
        self.ruta = ruta

    def exportar_html(self, carpeta):
        """Copia el archivo a la carpeta donde estaran las imagenes,
        y devuelve el html con la ruta de la imagen actualizada
        La carpeta ya debe estar creada
        """
        import os, shutil
        ristra = ""
        if self.ruta:
            (_, nombrefichero) = os.path.split(self.ruta)
            shutil.copyfile(self.ruta, carpeta + "/" + nombrefichero)
            ristra += "<img src=\"" + os.path.split(carpeta)[1] + "/" + nombrefichero + "\">"
        return ristra

    def html(self):
        """Devuelve la representación del objeto en html"""
        ristra = ""
        if self.ruta:
            ristra += "<img src=\"" + self.ruta + "\">"
        return ristra


