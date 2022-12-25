from Environment.Symbol import Symbol
from Environment.SymbolsTable import SymbolsTable
from Environment.Error import Error
from Environment.ListErrores import ListErrores
from Enum.typeExpression import typeExpression
import os

class Reportes():

    def __init__(self) -> None:
        super().__init__()
        self.Tabla = ""
        self.TablaErr = ""

    def generateTableSymbs(self):
        listado = SymbolsTable()

        tablaSimbolos = listado.getTablaSimbolos()
        print("----------> " + str(len(tablaSimbolos)))



        path = 'C:/Users/Cristian/Desktop/COMPI/2SV2022OLC2/TablaSimb.dot'

        with open(path, mode='w') as f:
            self.Tabla += "digraph G{ \n"
            self.Tabla += "Tabla [label = \" Tabla De Simbolos \", shape=component, color=\"/accent4/1:/accent4/4\", style=filled, fontsize=20.5]; \n"
            self.Tabla += "node [shape=plain] \n"
            self.Tabla += "TablaSimbolos [label=< \n"
            self.Tabla += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\"> \n"
            self.Tabla += "<tr><td><i><b>Nombre</b></i></td><td><i><b>Tipo</b></i></td><td><i><b>Ambito</b></i></td><td><i><b>Fila</b></i></td><td><i><b>Columna</b></i></td></tr> \n"
            
            for i in tablaSimbolos:
                objetoSimbolo:Symbol = i
                if(objetoSimbolo.type == typeExpression.BOOL or objetoSimbolo.type == typeExpression.INT or objetoSimbolo.type == typeExpression.FLOAT or objetoSimbolo.type == typeExpression.STRING ):
                    self.Tabla += "<tr><td><i><b>" + objetoSimbolo.id + "</b></i></td><td><i><b> VARIABLE </b></i></td><td><i><b>" + objetoSimbolo.ambito+ "</b></i></td><td><i><b>" + str(objetoSimbolo.fila) + "</b></i></td><td><i><b>" + str(objetoSimbolo.columna) + "</b></i></td></tr> \n"
                else :
                    self.Tabla += "<tr><td><i><b>" + objetoSimbolo.id + "</b></i></td><td><i><b> OTROS </b></i></td><td><i><b>" + objetoSimbolo.ambito+ "</b></i></td><td><i><b>" + str(objetoSimbolo.fila) + "</b></i></td><td><i><b>" + str(objetoSimbolo.columna) + "</b></i></td></tr> \n"
            
            
            self.Tabla += "</table>> \n"
            self.Tabla += "color=\"/accent6/1:/accent6/6\", style=filled]; \n"
            self.Tabla += "Tabla -> TablaSimbolos[arrowhead = diamond] \n"
            self.Tabla += "} \n"

            f.write(self.Tabla)

        os.system("dot -Tsvg TablaSimb.dot -o ReporteSimbolos.svg")

    
    def generateReporteErrores(self):
        listado = ListErrores()

        tablaErrores = listado.getTablaErrores()
        print("----------> " + str(len(tablaErrores)))
        contador = 0

        path = 'C:/Users/Cristian/Desktop/COMPI/2SV2022OLC2/TablaErrores.dot'

        with open(path, mode='w') as f:
            self.TablaErr += "digraph G{ \n"
            self.TablaErr += "Tabla [label = \" Tabla De Errores \", shape=component, color=\"/accent4/1:/accent4/4\", style=filled, fontsize=20.5]; \n"
            self.TablaErr += "node [shape=plain] \n"
            self.TablaErr += "TablaSimbolos [label=< \n"
            self.TablaErr += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\"> \n"
            self.TablaErr += "<tr><td><i><b>No.</b></i></td><td><i><b>Descripcion</b></i></td><td><i><b>Fila</b></i></td><td><i><b>Columna</b></i></td><td><i><b>Fecha-Hora</b></i></td></tr> \n"
            
            for i in tablaErrores:
                objetoSimbolo:Error = i
                self.TablaErr += objetoSimbolo.to_String(contador)
                contador += 1
            
            self.TablaErr += "</table>> \n"
            self.TablaErr += "color=\"/accent6/1:/accent6/6\", style=filled]; \n"
            self.TablaErr += "Tabla -> TablaSimbolos[arrowhead = diamond] \n"
            self.TablaErr += "} \n"

            f.write(self.TablaErr)

        os.system("dot -Tsvg TablaErrores.dot -o ReporteErrores.svg")