class Error:
    def __init__(self, descripcion, fila, columna, fechaHora):
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna
        self.fechaHora =fechaHora

    def to_String(self, index):
        return "<tr><td><i><b> " + str(index) + " </b></i></td><td><i><b> "+ str(self.descripcion) +" </b></i></td><td><i><b> "+ str(self.fila) +" </b></i></td><td><i><b> "+ str(self.columna) +" </b></i></td><td><i><b> "+ str(self.fechaHora) +" </b></i></td></tr>"