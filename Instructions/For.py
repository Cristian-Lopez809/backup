from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Enum.arithmeticOperation import arithmeticOperation
from Enum.relationalOperation import relationalOperation
from Environment.Environment import Environment
from Environment.Symbol import Symbol
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Expression.Arithmetic.PlusMinusModDivision import PlusMinusModDivision
from Expression.Primitive.NumberVal import NumberVal
from Expression.Primitive.VariableCall import VariableCall
from Expression.Relational.Relacional import Relacional
from Instructions.Asignacion import Asignacion
from Instructions.Declaration import Declaration

class For(Instruction):
    def __init__(self, fila, columna, declaracion:Declaration ,condition:Relacional, typeExpression:typeExpression,asignacionIncremento:Asignacion, block) -> None:
        super().__init__(fila,columna)
        self.condition = condition
        self.block = block
        self.declaracion=declaracion
        self.typeExpression = typeExpression
        self.asignacionIncremento=asignacionIncremento
        self.fila = fila
        self.columna = columna

    def compile(self, env:Environment) -> Value:
        if(self.typeExpression==typeExpression.INT):            
            #Declaración de variable
            newIncrementLabel = self.generator.newLabel()   

            self.declaracion.generator = self.generator
            self.condition.generator = self.generator
            self.asignacionIncremento.generator=self.generator
            
            valueDeclaration = self.declaracion.compile(env)

            newLabel = self.generator.newLabel()
            self.generator.addLabel(newLabel) 

            valueCondition = self.condition.compile(env)

            if(valueCondition.type == typeExpression.BOOL):
                self.generator.addLabel(valueCondition.trueLabel)

                newEnv = Environment(env, "Ciclo-For")
                newEnv.labelBrk = valueCondition.falseLabel
                newEnv.labelCont = newIncrementLabel
                for ins in self.block:
                    ins.generator = self.generator
                    ins.compile(newEnv)
                    
                self.generator.addGoto(newIncrementLabel)
                #incremento
                self.generator.addLabel(newIncrementLabel)    
                valueIncrement = self.asignacionIncremento.compile(env)
                self.generator.addGoto(newLabel)
                self.generator.addLabel(valueCondition.falseLabel)




