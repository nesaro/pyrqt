# Copyright (C) 2006-2026  Inmaculada Luengo Merino, Néstor Arocha Rodríguez
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

nombre = "Media de dos muestras independientes"
tipo = "Calculo"
etiquetas = ["Contraste de Hipotesis"]


# Inicializacion del widget
widget = {"tipo": "DiscriminadorCasoCasoVariable", "opciones": []}

# Definicion del formato de resultados
definicionresultado = [
    {
        "tipo": "Tabla",
        "nombre": "Descriptivo",
        "cabecera": [
            "Variable",
            "Caso",
            "Número de sujetos",
            "Media",
            "Desviación Típica",
        ],
        "numerofilas": 2,
    },
    {
        "tipo": "Tabla",
        "nombre": "Comparación de varianzas",
        "cabecera": [
            "Variable",
            "Caso1",
            "Caso2",
            "Significación",
            "Valor del estadistico",
        ],
    },
    {
        "tipo": "Tabla",
        "nombre": "Comparación de medias",
        "cabecera": [
            "Variable",
            "Caso1",
            "Caso2",
            "Varianzas",
            "Valor T obtenido",
            "Significación bilateral para T",
        ],
        "numerofilas": 2,
    },
]


# Funcion principal
def funcionprincipal(dato, comanda, opciones):
    from rpy import r  # pylint: disable=import-error

    diccionario = {}
    condicion1 = comanda[0][0] + "=" + comanda[0][1]
    condicion2 = comanda[0][0] + "=" + comanda[0][2]
    lista1 = dato.query(comanda[1], condicion1)
    lista2 = dato.query(comanda[1], condicion2)
    lateral = "two.sided"
    resultadoigual = r.t_test(lista1, lista2, var_equal=True, alt=lateral)
    resultadodif = r.t_test(lista1, lista2, var_equal=False, alt=lateral)

    diccionario["Comparación de medias"] = {}
    diccionario["Comparación de medias"][0] = {}
    diccionario["Comparación de medias"][1] = {}
    diccionario["Comparación de medias"][0]["Variable"] = comanda[1]
    diccionario["Comparación de medias"][0]["Caso1"] = dato.resolver_etiqueta(
        comanda[0][0], int(comanda[0][1])
    )
    diccionario["Comparación de medias"][0]["Caso2"] = comanda[0][2]
    diccionario["Comparación de medias"][0]["Varianzas"] = "Se asume igual"
    diccionario["Comparación de medias"][0]["Significación bilateral para T"] = (
        resultadoigual["p.value"]
    )
    diccionario["Comparación de medias"][0]["Valor T obtenido"] = resultadoigual[
        "statistic"
    ]["t"]
    diccionario["Comparación de medias"][1]["Variable"] = comanda[1]
    diccionario["Comparación de medias"][1]["Caso1"] = comanda[0][1]
    diccionario["Comparación de medias"][1]["Caso2"] = comanda[0][2]
    diccionario["Comparación de medias"][1]["Varianzas"] = "Se asume distinta"
    diccionario["Comparación de medias"][1]["Significación bilateral para T"] = (
        resultadodif["p.value"]
    )
    diccionario["Comparación de medias"][1]["Valor T obtenido"] = resultadodif[
        "statistic"
    ]["t"]
    diccionario["Descriptivo"] = {}
    diccionario["Descriptivo"][0] = {}
    diccionario["Descriptivo"][0]["Variable"] = comanda[1]
    diccionario["Descriptivo"][0]["Caso"] = comanda[0][1]
    diccionario["Descriptivo"][0]["Número de sujetos"] = len(lista1)
    diccionario["Descriptivo"][0]["Media"] = r.mean(lista1)
    diccionario["Descriptivo"][0]["Desviación Típica"] = r.sd(lista1)
    diccionario["Descriptivo"][1] = {}
    diccionario["Descriptivo"][1]["Variable"] = comanda[1]
    diccionario["Descriptivo"][1]["Caso"] = comanda[0][2]
    diccionario["Descriptivo"][1]["Número de sujetos"] = len(lista2)
    diccionario["Descriptivo"][1]["Media"] = r.mean(lista2)
    diccionario["Descriptivo"][1]["Desviación Típica"] = r.sd(lista2)
    diccionario["Comparación de varianzas"] = {}
    diccionario["Comparación de varianzas"]["Variable"] = comanda[1]
    diccionario["Comparación de varianzas"]["Caso1"] = comanda[0][1]
    diccionario["Comparación de varianzas"]["Caso2"] = comanda[0][2]
    diccionario["Comparación de varianzas"]["Significación"] = r.var_test(
        lista1, lista2
    )["p.value"]
    diccionario["Comparación de varianzas"]["Valor del estadistico"] = r.var_test(
        lista1, lista2
    )["statistic"]["F"]
    return diccionario


def funcionchequeoentradausuario(opciones):
    return True


def funcionchequeocondiciones(interfazdato):
    if len(interfazdato.lista_tit_discreto) < 1:
        return False
    if len(interfazdato.lista_tit_numerica) < 1:
        return False
    return True
