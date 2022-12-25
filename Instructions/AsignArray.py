from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class AsignArray(Instruction):

    def __init__(self, fila, columna,  id:str, indice:str, exp: Expression) -> None:
        super().__init__(fila,columna)
        self.id = id
        self.indice = indice
        self.exp = exp
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        self.exp.generator = self.generator
        
        newValue: Value = self.exp.compile(environment)
        oldVar: Symbol = environment.getVariable(self.id)

        if oldVar != None:
            if(oldVar.type != typeExpression.UNDEFINED):
                if(oldVar.type == typeExpression.LIST_INTFL and (newValue.type == typeExpression.INT or newValue.type == typeExpression.INT)):
                    print("Match Type LIST")
                    contArray = int(oldVar.position)

                    #temp valores in array
                    newTemp2 = self.generator.newTemp()
                    self.generator.addExpression(str(newTemp2), str(contArray), "1", "+")

                    
                    #temp indice array
                    tempCont = self.generator.newTemp()
                    self.generator.addExpression(str(tempCont), str(1), "", "")


                    newLabel = self.generator.newLabel()
                    self.generator.addLabel(newLabel)

                    newTemp = self.generator.newTemp()
                    self.generator.addGetStack(newTemp,str(newTemp2))

                    #label coincidem¡n
                    labelTrue = self.generator.newLabel()

                    outLabel = self.generator.newLabel()#false
                    self.generator.addIf(newTemp, "-1" , "==", outLabel)
                    self.generator.addIf(tempCont, str(self.indice), "==", labelTrue)
                    self.generator.addExpression(str(newTemp2), str(newTemp2), "1", "+")
                    self.generator.addExpression(str(tempCont), str(tempCont), "1", "+")
                    self.generator.addGoto(newLabel)
                    #label todo nice
                    self.generator.addLabel(labelTrue)
                    self.generator.addSetStack(str(newTemp2), newValue.getValue())
                    #label no hace nada
                    self.generator.addLabel(outLabel)
                    self.generator.addPrintf("c", str(93))

                else:
                    objErrores.setNewError(Error("Error: el tipo de dato no coincide con el especificado", self.fila, self.columna, dt_string))   
                    print("Error: no hizo match con los tipos")
            else:#asignacion de var pre-declarada
                oldVar.setType(newValue.type)
                self.generator.addSetStack(str(oldVar.position), str(newValue.getValue()))
        else:
            objErrores.setNewError(Error("Error: la variable a asignar no existe", self.fila, self.columna, dt_string))   
            print("Error: La variable a asignar no existe")