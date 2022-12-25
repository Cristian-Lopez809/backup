from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression


class And(Expression):

    def __init__(self, fila, columna,  left: Expression, right: Expression) -> None:
        super().__init__(fila,columna)
        self.leftExpression = left
        self.rightExpression = right
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:

        self.leftExpression.generator = self.generator
        self.rightExpression.generator = self.generator

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        leftValue: Value = self.leftExpression.compile(environment)#ejecuta izquierdo
        
        if leftValue != None:

            if (leftValue.type == typeExpression.BOOL):

                self.generator.addLabel(leftValue.trueLabel)#cumple el primero
                rightValue: Value = self.rightExpression.compile(environment)#ejecuta el segundo

                if rightValue != None:

                    if (leftValue.type == typeExpression.BOOL):
                        self.generator.addLabel(leftValue.falseLabel)
                        self.generator.addLabel(rightValue.falseLabel)
    
                        newLabel = self.generator.newLabel()
                        self.generator.addGoto(newLabel)
    
    
                        newValue = Value("", False, typeExpression.BOOL)
    
                        newValue.trueLabel = rightValue.trueLabel
                        newValue.falseLabel = newLabel
    
                        return newValue
                else:
                    objErrores.setNewError(Error("Error: expresion de tipo None", self.fila, self.columna, dt_string))   
        else:
            objErrores.setNewError(Error("Error: expresion de tipo None", self.fila, self.columna, dt_string))   
