class Symbol:
    def __init__(self, id: str, type, position, fila, columna, ambito):
        self.id = id
        self.type = type
        self.position = position
        self.fila = fila
        self.columna = columna
        self.ambito =ambito

    def getId(self):
        return self.id

    def getValue(self):
        return self.value

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type
    
