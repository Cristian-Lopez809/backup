from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression


class Or(Expression):

    def __init__(self, fila, columna,  left: Expression, right: Expression) -> None:
        super().__init__(fila,columna)
        self.leftExpression = left
        self.rightExpression = right
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()
        self.leftExpression.generator = self.generator
        self.rightExpression.generator = self.generator

        leftValue: Value = self.leftExpression.compile(environment)
        
        if leftValue != None:

            if (leftValue.type == typeExpression.BOOL):
                self.generator.addLabel(leftValue.falseLabel)#no cumple izq
                rightValue: Value = self.rightExpression.compile(environment)#ejec derecho

                if rightValue != None:
                    self.generator.addLabel(leftValue.trueLabel)#cuando son verdaderos
                    self.generator.addLabel(rightValue.trueLabel)
                    newLabel = self.generator.newLabel()
                    self.generator.addGoto(newLabel)
    
                    newValue = Value("", False, typeExpression.BOOL)
    
                    newValue.trueLabel = newLabel
                    newValue.falseLabel = rightValue.falseLabel
                    return newValue
                else:
                    objErrores.setNewError(Error("Error: expresion de tipo None", self.fila, self.columna, dt_string))   
        else:
            objErrores.setNewError(Error("Error: expresion de tipo None", self.fila, self.columna, dt_string))   
