from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Enum.arithmeticOperation import arithmeticOperation

class PlusMinusModDivision(Expression):

    def __init__(self, fila, columna,  left: Expression, right: Expression, operation:arithmeticOperation):
        super().__init__(fila,columna)
        self.leftExpression = left
        self.rightExpression = right
        self.operationOption=operation
        self.fila = fila
        self.columna = columna

    def compile(self,environment:Environment)->Value:
        self.leftExpression.generator = self.generator
        self.rightExpression.generator = self.generator
        self.operationOption=self.operationOption

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        leftValue:Value=self.leftExpression.compile(environment)
        rightValue:Value=self.rightExpression.compile(environment)

        op = ''
        if self.operationOption == arithmeticOperation.PLUS:
            op = '+'
        elif self.operationOption == arithmeticOperation.MINUS:
            op = '-'
        elif self.operationOption == arithmeticOperation.DIV:
            op = '/'
        elif self.operationOption == arithmeticOperation.MODULE:
            op = '%'

        newTemp = self.generator.newTemp()

        if(leftValue.type==typeExpression.INT):
            if(rightValue.type==typeExpression.INT or rightValue.type==typeExpression.FLOAT):
                self.generator.addExpression(newTemp,leftValue.getValue(),rightValue.getValue(),op)
                return Value(newTemp,True,rightValue.type)
            else:                
                objErrores.setNewError(Error("Error Aritmetico: tipos de datos incorrectos ", self.fila, self.columna, dt_string))  
                print("Error")
        
        elif(leftValue.type==typeExpression.FLOAT):
            if(rightValue.type==typeExpression.INT or rightValue.type==typeExpression.FLOAT):
                self.generator.addExpression(newTemp,leftValue.getValue(),rightValue.getValue(),op)
                return Value(newTemp,True,leftValue.type)
            else:                
                objErrores.setNewError(Error("Error Aritmetico: tipos de datos incorrectos ", self.fila, self.columna, dt_string))  
                print("Error")
        
        elif(leftValue.type==typeExpression.STRING):
            if(rightValue.type==typeExpression.STRING):
                self.generator.addExpression(newTemp,leftValue.getValue(),rightValue.getValue(),op)
                return Value(newTemp,True,leftValue.type)
            else:                
                objErrores.setNewError(Error("Error Aritmetico: tipos de datos incorrectos ", self.fila, self.columna, dt_string))  
                print("Error")
        else:
                objErrores.setNewError(Error("Error Aritmetico: tipos de datos incorrectos ", self.fila, self.columna, dt_string))  
                print("Error Aritmetico")
                return Value("0",False,TypeError.INTEGER)

