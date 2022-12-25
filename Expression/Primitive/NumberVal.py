from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class NumberVal(Expression):

    def __init__(self, fila, columna,  type: typeExpression, value) -> None:
        super().__init__(fila,columna)
        self.type = type
        self.value = value
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        if(self.type == typeExpression.INT or self.type == typeExpression.FLOAT):
            return Value(str(self.value),False,self.type)

        objErrores.setNewError(Error("Error: no se reconoce el tipo de dato", self.fila, self.columna, dt_string))   
        print("No se reconoce el tipo")
        return Value("0",False,typeExpression.INT)