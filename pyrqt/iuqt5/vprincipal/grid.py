#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2018   Néstor Arocha Rodríguez

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

"""Grid y clases asociadas"""
from PyQt4 import QtCore,QtGui
from PyQt4.QtGui import QMessageBox, QComboBox, QInputDialog
from pyrqt.datos.variables import * #Para poder preguntar por todos los tipos
import logging
LOG = logging.getLogger("__name__")

class  Grid(QtGui.QTabWidget):
    """La tabla que manejara los registros y las variables"""

    #Funciones de inicializacion
    def __init__(self, padre, interfazdatos, porterodatos):
        from pyrqt.datos.conversion import AgenteConversion
        self.__portero = porterodatos
        QtGui.QTabWidget.__init__(self)#,padre)
        #TODO Pendiente portabilidad qt4
        self.setTabPosition(QtGui.QTabWidget.South)
        self.tab = QtGui.QWidget(self)
        #TODO Pendiente portabilidad qt4
        tabLayout = QtGui.QVBoxLayout(self.tab)#,11,6,"tabLayout")
        self.table1 = QtGui.QTableWidget(self.tab)
        tabLayout.addWidget(self.table1)
        self.insertTab(0, self.tab, "&Registros")
        self.tab_2 = QtGui.QWidget(self)
        tabLayout_2 = QtGui.QVBoxLayout(self.tab_2)#,11,6,"tabLayout_2")
        self.table2 = QtGui.QTableWidget(self.tab_2)
        tabLayout_2.addWidget(self.table2)
        self.insertTab(1,self.tab_2,"&Variables")
        self.modoetiqueta = False # Variable que guarda si estamos en modo etiqueta o normal

        self.__nreg = 10 
        self.__nvar = 10
        self.__idu = interfazdatos
        self.__init_t_reg()
        self.__init_t_var()
        self.__conexiones()
        self.__agenteconversion = AgenteConversion(self.__idu)
        

    def __init_t_reg(self):
        """Inicializa la tabla de datos"""
        self.table1.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table1.setColumnCount(16) 
        self.table1.setRowCount(64)
        qstringvacio=''
        qstringlist=[]
        for x in range(self.table1.horizontalHeader().count()):
            qstringlist.append(qstringvacio)
        self.table1.setHorizontalHeaderLabels(qstringlist)


    def __init_t_var(self):
        """Inicializa la tabla de variables"""
        self.table2.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table2.setRowCount(self.__nvar)
        self.table2.setColumnCount(4)
        qstringlist = []
        qstringlist.append("Nombre")
        qstringlist.append("Tipo")
        qstringlist.append("Valor por defecto")
        qstringlist.append("Etiqueta")
        self.table2.setHorizontalHeaderLabels(qstringlist)

    def __conexiones(self):
        """Conexiones"""
        from PyQt4.QtCore import SIGNAL
        self.connect(self.table1, SIGNAL("cellChanged(int,int)"),self.__modificacion_t_reg)
        self.connect(self.table2, SIGNAL("cellChanged(int,int)"),self.__modificacion_t_var)
    #FUNCIONES SHOW

    def myUpdate(self):
        """Actualizacion de contenido"""
        LOG.debug("Actualizando contenido del grid")
        self.__mostrar_t_reg()
        self.__mostrar_t_var()

    def showEvent(self, ev):
        """Redefinición del show de la clase base"""
        self.myUpdate()
        QtGui.QTabWidget.showEvent(self,ev)
        
    def borrar_seleccion(self, borrardatos=False):
        """Esta funcion borra la seleccion de la tabla. 
        El parametro opcional determina si se ha deborrar tambien los datos"""
        tablaactual = self.currentPageIndex()
        if tablaactual == 0:
            tabla = self.table1
        else:
            tabla = self.table2
        if borrardatos:
            lista = []
            for seleccion in range(tabla.numSelections()):
                for fila in range(tabla.selection(seleccion).topRow(), tabla.selection(seleccion).bottomRow()+1):
                    lista.append(fila)
            lista.sort()
            lista.reverse()
            for fila in lista:
                if tablaactual == 0:
                    if fila < self.__idu.n_reg:
                        del self.__idu[fila]
                else:
                    if fila < self.__idu.n_var:
                        self.__idu.delVar(fila)

        for seleccion in range(tabla.numSelections()):
            tabla.removeSelection(seleccion)

    def lista_seleccion(self, tabla=0):
        """Devuelve una lista con los registros que han sido seleccionados"""
        tabla = self.table1
        listasalida = []
        if tabla.numSelections():
            toprow = tabla.numRows()
            bottomrow = 0
            leftcol = tabla.numCols()
            rightcol = 0
            for seleccion in range(tabla.numSelections()):
                misel = tabla.selection(seleccion)
                if misel.topRow() < toprow: 
                    toprow = misel.topRow()
                if misel.bottomRow()> bottomrow: 
                    bottomrow = misel.bottomRow()
                if misel.leftCol()< leftcol: 
                    leftcol = misel.leftCol()
                if misel.rightCol()> rightcol: 
                    rightcol = misel.rightCol()
                LOG.debug("Limites totales de seleccion:("+str(toprow)+","+str(leftcol)+")")
                LOG.debug("Limites totales de seleccion:("+str(bottomrow)+","+str(rightcol)+")")
            if bottomrow >= self.__idu.n_reg:
                bottomrow = self.__idu.n_reg - 1
            if rightcol >= self.__idu.n_var:
                rightcol = self.__idu.n_var - 1
            for fila in range(toprow, bottomrow+1):
                nuevafila = []
                for columna in range(leftcol, rightcol+1):
                    if self.__idu[fila][columna].valido() and tabla.isSelected(fila, columna):
                        nuevafila.append(repr(self.__idu[fila][columna]))
                    else:
                        nuevafila.append(None)
                LOG.debug("Fila añadida a la seleccion de copiado: "+str(nuevafila))
                listasalida.append(nuevafila)
        return listasalida


    def __mostrar_t_var(self):  
        """ Representa la variable pos en la tabla de variables. Las propiedades de la variable las lee de los datos.
        Si no se indica posicion, se entiende que se quiere rellenar toda la tabla
        """
        LOG.debug("Actualizando tabla de variables completa")
        if self.__nvar > (self.table2.rowCount()-self.__idu.n_var):
            self.table2.setRowCount(self.__idu.n_var + self.__nvar)
        for fila in range(self.__idu.n_var, self.table2.rowCount()):
            for columna in range(self.table2.columnCount()):
                pass #Limpiar 
        for indicevar in range(self.__idu.n_var):
            self.__mostrar_var(indicevar)
        self.__mostrar_titulo_t_reg()

    def __mostrar_var(self, pos):
        """Muestra una unica variable (fila) en la tabla segun el listado de variables"""
        variable = self.__idu.var(pos)
        #self.table2.item(pos,0).setText(str(variable.nombre))
        if not(self.table2.item(pos,0) and str(variable.name)==self.table2.item(pos,0).text()):
            self.table2.setItem(pos,0,QtGui.QTableWidgetItem(str(variable.name)))
        newcombo = self.__combotableitem()
        self.table2.setCellWidget(pos,1, newcombo)    
        #self.table2.item(pos,1).setCurrentItem(variable.tipo)
        newcombo.setCurrentIndex(newcombo.findText(variable.tipo))
        if not(self.table2.item(pos,2) and str(variable.valorpordefecto)==self.table2.item(pos,2).text()):
            self.table2.setItem(pos,2,QtGui.QTableWidgetItem(str(variable.valorpordefecto)))
        if not(self.table2.item(pos,3) and str(variable.descripcion)==self.table2.item(pos,3).text()):
            self.table2.setItem(pos,3,QtGui.QTableWidgetItem(str(variable.descripcion)))

    def __mostrar_t_reg(self):
        """ 
        Rellena la tabla de datos con los registros actuales
        """
        if self.__nreg > (self.table1.rowCount() - self.__idu.n_reg):
            self.table1.setRowCount(self.__idu.n_reg + self.__nreg)
        for i in range(self.__idu.n_reg):
            self.__mostrar_reg(i)
        self.__mostrar_titulo_t_reg()
        for i in range(self.__idu.n_reg, self.table1.rowCount()):
            for j in range(self.table1.columnCount()):
                #TODO Pendiente portabilidad qt4
                #self.table1.clearCell(x,y)
                pass #LIMPIAR
        for i in range(self.table1.rowCount()):
            for j in range(self.__idu.n_var, self.table1.columnCount()):
                pass #Introducir contenido
        self.__mostrar_lateral_t_reg()

    def __mostrar_reg(self, pos):
        """Muestra un solo dato"""
        for i in range(self.__idu.n_var):
            if not(self.table1.item(pos,i) and str(self.__idu[pos][i])==self.table1.item(pos,i).text()):
                self.table1.setItem(pos,i,QtGui.QTableWidgetItem(str(self.__idu[pos][i])))

    def __mostrar_columna_t_reg(self, pos):
        """Muestra una columna de la tabla de registros"""
        for i in range(self.__idu.n_reg):
            if not self.table1.item(i,pos) or  str(self.__idu[i][pos]) != self.table1.item(i,pos).text():
                self.table1.setItem(i,pos,QtGui.QTableWidgetItem(str(self.__idu[i][pos])))


    def __mostrar_titulo_t_reg(self, pos=None):
        """Actualiza los titulos de la tabla de datos segun las variables"""
        if pos:
            self.table1.setHorizontalHeaderItem(pos,QtGui.QTableWidgetItem(self.__idu.var(pos).name))
        else:
            qstringlist=[]
            qstringvacio=''
            i = 0
            for x in range(self.__idu.n_var):
                qstringlist.append(self.__idu.var(i).name)
                i += 1

            for x in range(self.__idu.n_var, self.table1.horizontalHeader().count()):
                qstringlist.append(qstringvacio)
            self.table1.setHorizontalHeaderLabels(qstringlist)

    def __mostrar_lateral_t_reg(self):
        """Muestra los numeros laterales. Sirve para el filtrado"""
        qstringlist=[]
        #lista=self.__idu.getCol(self.__gestorfiltro.variable,filtrado=False)
        for i in range(self.__idu.n_reg):
        #    if self.__gestorfiltro.variable and not lista[i]:
        #        lateral.setLabel(i,"--"+str(i))
        #    else:
            qstringlist.append(str(i+1))
        self.table1.setVerticalHeaderLabels(qstringlist)

    def __combotableitem(self):
        """Devuelve un nuevo objeto tipo combotableitem con la lista de tipos"""
        lista = []
        from pyrqt.listas import SL
        from PyQt4.QtCore import SIGNAL
        for tipo in SL.nombrevariables:
            lista.append(tipo)
        combo = QComboBox()
        combo.addItems(lista)
        self.connect(combo, SIGNAL("currentIndexChanged(const QString &)"),self.__modificacion_combotableitem)
        return combo#self.table2)#,lista)
    
        
    def __modificacion_t_var(self, fila, columna):
        """Funcion a que conecta con la introduccion de nuevos datos en la tabla de variables"""
        if self.table2.currentRow()!=fila or self.table2.currentColumn()!=columna: return
        LOG.debug("Modificacion detectada en la tabla de variables")
        self.__portero.guardar_estado()
        if fila >= self.__idu.n_var: #Es una nueva variable
            #Variables intermedias (creadas con los valores por defecto)
            for valorintermedio in range (self.__idu.n_var, fila):
                self.__insertar_variable()
                self.__mostrar_var(valorintermedio)
            self.__insertar_variable()
        #Variable modificada
        variable = self.__idu.var(fila)
        if columna == 1:   # El usuario quiere cambiar el tipo
            from pyrqt.datos import variables
            textoencuestion = str(self.table2.cellWidget(fila, columna).currentText() )
            #preguntar el tipo de conversion
            metododeseado = self.__preguntar_conversion(variable,textoencuestion)
            if metododeseado:
                pareja= self.__agenteconversion(variable,textoencuestion,metododeseado) #Pareja variable-list
                self.__idu.setVar(fila, pareja[0],pareja[1])
                self.__mostrar_t_reg()  
        else: #Restos de campos (Texto)
            from pyrqt.excepciones import VariableExisteException
            try:
                self.__idu.modificar_var(variable, columna ,str(self.table2.item(fila,y).text()))
            except VariableExisteException:
                QMessageBox.warning(self, u'Atención', u'El nombre de variable ya existe')

        self.__mostrar_var(fila)
        #En todos los casos, actualizamos el titulo de la tabla de datos
        self.__mostrar_titulo_t_reg()

    def __actualizar_reg_interfazdatos(self, row, col, valor):
        """actualiza un dato en interfazdatos,recogiendo la excepcion en caso de error """
        LOG.debug("Actualizando datos de la interfaz:" + str(row) + "," + str(col))
        try:
            self.__idu[row][col] = str(valor)
        except ValueError:
            QMessageBox.warning(self, 'Atención', u'El dato no es válido')
    
    def __insertar_registro(self):
        """Inserta un registro genérico, y ademas comprueba que no nos estamos acercando al final de la tabla"""
        self.__idu.ana_reg()
        if self.__nreg > (self.table1.rowCount() - self.__idu.n_reg):
            self.table1.setRowCount(self.table1.rowCount()+1)

    def __insertar_variable(self):
        """Inserta una variable genérica, y ademas comprueba que no nos acercamos a ninguno de los limites de las tablas"""
        self.__idu.ana_var()
        if self.__nvar > (self.table2.rowCount() - self.__idu.n_var):
            self.table2.setRowCount(self.table2.rowCount() + 1)
            self.table1.setColumnCount(self.table1.columnCount() + 1)

    def __modificacion_t_reg(self, fila, columna):
        """Actualiza los datos del objeto dato a partir de un cambio en la tabla de datos"""
        if self.table1.currentRow()!=fila or self.table1.currentColumn()!= columna: return
        if (fila < self.__idu.n_reg)\
                and (columna < self.__idu.n_var)\
                and (self.table1.item(fila, columna).text() == str(self.__idu[fila][columna])):
            return
        LOG.debug("Cambiado registro en la tabla")
        valor = self.table1.item(fila, columna).text()
        self.__portero.guardar_estado()
        rango = None
        if columna >= self.__idu.n_var:
            LOG.debug("Creando nueva variable por demanda en la modificaicon de un registro")
            #Estamos trabajando sobre una variable inexistente
            rango = range(self.__idu.n_var, columna + 1)
            for i in rango:
                self.__insertar_variable()
            self.__mostrar_t_var() #actualizamos la tabla de variables
        if fila >= self.__idu.n_reg:
            #no existen registros intermedios
            LOG.debug("Creando nuevo registro por demanda en la modificaicon de un registro")
            for i in range (self.__idu.n_reg, fila):
                self.__insertar_registro()
                self.__mostrar_reg(i)  
            self.__idu.ana_reg() #El último se separa, tenemos que verificar si el usuario ha escrito correctamente
        if rango:
            for i in rango:
                LOG.debug("MOSTRANDO COLUMNA!")
                self.__mostrar_columna_t_reg(i)
        self.__actualizar_reg_interfazdatos(fila, columna, valor)
        self.__mostrar_reg(fila)
        #Comprobacion de que sobra el numero correcto de celdas
        if self.__nreg > (self.table1.rowCount() - self.__idu.n_reg):
            self.table1.setRowCount(self.__idu.n_reg + self.__nreg)
        self.parent().parent().parent().mostrar_undo_redo() #FIXME... que son todos estos parent?

    
    def __preguntar_conversion(self, variable, objetivo):
        """Pregunta cual de los metodos disponibles para la conversion desea escoger el usuario"""
        if not isinstance(objetivo, str):
            LOG.debug("__preguntar_conversion: Bad type for string: "+str(objetivo.__class__))
            raise TypeError
        lista = []
        if "Agrupador" in variable.diccionarioconversion:
            #Conversión a todos los tipos
            lista += variable.diccionarioconversion["Agrupador"]
        for tipo in variable.diccionarioconversion.iterkeys():
            if tipo == objetivo:
                lista += variable.diccionarioconversion[tipo]
        #Elaborar una lista y preguntar al usuario
        qlista = []
        for elemento in lista:
            qlista.append(elemento)
        cadena = QInputDialog.getItem(self, "Elige!", u"Elige una función de conversion", qlista, 0, False)
        #devolver el nombre de la funcion
        if cadena[1]:
            return str(cadena[0])
        else:
            return ""

    def __modificacion_combotableitem(self):
        """Que hacer cuando se modifica el texto de un combobox?"""
        self.__modificacion_t_var(self.table2.currentRow(), 1)
