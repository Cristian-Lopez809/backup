from Grammar.gramatica import parser
from Reportes import Reportes


def start():
    Reporte = Reportes()
    f = open("./entrada.txt", "r")
    input = f.read()
    C3D = parser.parse(input)
    #Reporte.generateTableSymbs()
    #Reporte.generateReporteErrores()

    f2 = open("./salida.go","w")
    f2.write(C3D)

if __name__ == "__main__":
    start()