from Environment.Symbol import Symbol

tablaSimbolos = []

class SymbolsTable:
    def __init__(self):
        print("")

    def setNewSimbol(self, simbolo : Symbol):
        tablaSimbolos.append(simbolo)

    def getTablaSimbolos(self):
        return tablaSimbolos
    