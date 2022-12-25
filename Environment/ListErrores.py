from Environment.Error import Error

tablaErrores = []

class ListErrores:
    def __init__(self):
        self

    def setNewError(self, error : Error):
        tablaErrores.append(error)

    def getTablaErrores(self):
        return tablaErrores
