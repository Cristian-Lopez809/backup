from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Enum.relationalOperation import relationalOperation

class Relacional(Expression):

    def __init__(self, fila, columna,  left: Expression, right: Expression, op: relationalOperation) -> None:
        super().__init__(fila,columna)
        self.leftExpression = left
        self.rightExpression = right
        self.op = op
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        self.leftExpression.generator = self.generator
        self.rightExpression.generator = self.generator

        leftValue: Value = self.leftExpression.compile(environment)
        rightValue: Value = self.rightExpression.compile(environment)

        if(leftValue.type == typeExpression.INT or leftValue.type == typeExpression.FLOAT):

            if(rightValue.type == typeExpression.INT or rightValue.type == typeExpression.FLOAT):

                newValue = Value("",False,typeExpression.BOOL)

                if(self.trueLabel == ""):
                    self.trueLabel = self.generator.newLabel()
                
                if(self.falseLabel == ""):
                    self.falseLabel = self.generator.newLabel()

                if(self.op == relationalOperation.DIFERENTE):
                    self.generator.addIf(leftValue.value, rightValue.value, "!=",self.trueLabel)
                    self.generator.addGoto(self.falseLabel)
                elif(self.op == relationalOperation.IGUAL):
                    self.generator.addIf(leftValue.value, rightValue.value, "==",self.trueLabel)
                    self.generator.addGoto(self.falseLabel)
                elif(self.op == relationalOperation.MAYOR):
                    self.generator.addIf(leftValue.value, rightValue.value, ">",self.trueLabel)
                    self.generator.addGoto(self.falseLabel)
                elif(self.op == relationalOperation.MAYORIGUAL):
                    self.generator.addIf(leftValue.value, rightValue.value, ">=",self.trueLabel)
                    self.generator.addGoto(self.falseLabel)
                elif(self.op == relationalOperation.MENOR):
                    self.generator.addIf(leftValue.value, rightValue.value, "<",self.trueLabel)
                    self.generator.addGoto(self.falseLabel)
                elif(self.op == relationalOperation.MENORIGUAL):
                    self.generator.addIf(leftValue.value, rightValue.value, "<=",self.trueLabel)
                    self.generator.addGoto(self.falseLabel)
                else:
                    objErrores.setNewError(Error("Error: Operacion-Relacional", self.fila, self.columna, dt_string))   
                    return print("error En Relacionales")

                newValue.trueLabel = self.trueLabel
                newValue.falseLabel = self.falseLabel

                return newValue

            