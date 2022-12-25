from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression


class Not(Expression):

    def __init__(self, fila, columna,  right: Expression) -> None:
        super().__init__(fila,columna)
        self.rightExpression = right
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        self.rightExpression.generator = self.generator

        rightValue: Value = self.rightExpression.compile(environment)

        if rightValue != None:
            if (rightValue.type == typeExpression.BOOL):

                newValue = Value("", False, typeExpression.BOOL)

                newValue.trueLabel = rightValue.falseLabel
                newValue.falseLabel = rightValue.trueLabel
                return newValue
        else:
            objErrores.setNewError(Error("Error: expresion de tipo None", self.fila, self.columna, dt_string))   
            print("Error: la expresion es null en not")
