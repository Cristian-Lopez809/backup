from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class Continue(Instruction):

    def __init__(self,  fila, columna ) -> None:
        super().__init__(fila,columna)
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        if environment.labelCont == '':
            objErrores.setNewError(Error("Error: Instruccion continue fuera de ciclo", self.fila, self.columna, dt_string))   
            print('Continue fuera de ciclo')
            return
        
        self.generator.addGoto(environment.labelCont)
