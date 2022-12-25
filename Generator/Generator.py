
class Generator:

    def __init__(self) -> None:
        self.generator = None
        self.temporal = 0
        self.label = 0
        self.code = []
        self.tempList = []
        self.funcionesCode = []
        self.funcNativas = []
        self.funcionIn = False
        self.toUpper = False
        self.inNatives = False
        self.printStr = False
        self.toLower = False

    #Obtener los temporales usados
    def getUsedTemps(self) -> str:
        return ",".join(self.tempList)
    
    #Introduccion de Codigo segun ambito
    def definitionCode(self, code):
        if(self.inNatives):
            if len(self.funcNativas) == 0: 
                self.funcNativas.append(code)
            else:
                self.funcNativas.append("\t" + code)
        elif(self.funcionIn):
            if len(self.funcionesCode) == 0: 
                self.funcionesCode.append(code)
            else:
                self.funcionesCode.append("\t" + code)
        else:
            self.code.append("\t" + code)

    #Obtener el codigo generado
    def getCode(self) -> str:
        tempCode: str = 'package main\n'
        tempCode = tempCode + 'import("fmt")\n\n'
        tempCode = tempCode + "var HEAP[1000]float64\n"
        tempCode = tempCode + "var STACK[1000]float64\n"
        tempCode = tempCode + "var P, H float64\n"

        if(len(self.tempList) > 0):
            tempCode = tempCode + "var " + self.getUsedTemps() + " float64;\n\n"

        tempCode = tempCode + self.print_true_proc()
        tempCode = tempCode + self.print_false_proc()

        tempCode = tempCode + '\n'.join(self.funcNativas)

        tempCode = tempCode + '\n'.join(self.funcionesCode)

        tempCode = tempCode + '\nfunc main(){\n'
        tempCode = tempCode + "\n".join(self.code)
        tempCode = tempCode + '\n}\n'
        
        return tempCode
    
    #Generar print Booleans
    def print_true_proc(self):
        cadena = "\nfunc print_true_proc() {\n"
        cadena += "fmt.Printf(\"True\")\n"
        cadena += "}\n"

        return cadena

    def print_false_proc(self):
        cadena = "\nfunc print_false_proc() {\n"
        cadena += "fmt.Printf(\"False\")\n"
        cadena += "}\n"

        return cadena

    #Generar un nuevo temporal
    def newTemp(self) -> str:
        temp = "t" + str(self.temporal)
        self.temporal = self.temporal + 1

        #Lo guardamos para declararlo
        self.tempList.append(temp)
        return temp

    #Generador de label
    def newLabel(self) -> str:
        temp = self.label
        self.label = self.label + 1
        return "L" + str(temp)

    def addCallFunc(self, name: str):
        #self.code.append(name + "();")
        self.definitionCode(name + "();")

    #Añade label al codigo
    def addLabel(self, label: str):
        #self.code.append(label + ":")
        self.definitionCode(label + ":")

    def addExpression(self, target: str, left: str, right: str, operator: str):
        #self.code.append(target + " = " + left + " " + operator + " " + right)
        self.definitionCode(target + " = " + left + " " + operator + " " + right)

    def addIf(self, left: str, rigth: str, operator: str, label: str):
        #self.code.append("if(" + left + " " + operator + " " + rigth + ") {goto " + label + ";}")
        self.definitionCode("if(" + left + " " + operator + " " + rigth + ") {goto " + label + ";}")

    def addIfNot(self, rigth: str):
        #self.code.append("if(!" + rigth + ") { }")
        self.definitionCode("if(!" + rigth + ") { }")


    def addGoto(self, label:str):
        #self.code.append("goto " + label + ";")
        self.definitionCode("goto " + label + ";")

    #Añade un printf
    def addPrintf(self, typePrint:str, value:str):
        #self.code.append("fmt.Printf(\"%" + typePrint + "\"," + value + ")")
        self.definitionCode("fmt.Printf(\"%" + typePrint + "\", int(" + value + "))")

    #Salto de linea  ***********************************************************************
    def addNewLine(self):
        #self.code.append('fmt.Printf(\"%c\",10);')
        self.definitionCode('fmt.Printf(\"%c\",int(10));')

    #Se mueve hacia la posicion siguiente del heap
    def addNextHeap(self):
        #self.code.append("H = H + 1;")
        self.definitionCode("H = H + 1;")
    
    #Se mueve hacia la posicion siguiente del stack
    def addNextStack(self,index:str):
        #self.code.append("P = P + " + index + ";")
        self.definitionCode("P = P + " + index + ";")    

    #Se mueve hacia la posicion anterior del stack
    def addBackStack(self, index:str):
        #self.code.append("P = P - " + index + ";")
        self.definitionCode("P = P - " + index + ";")

    #Obtiene el valor del heap en cierta posicion
    def addGetHeap(self, target:str, index: str):
        #self.code.append(target + " = HEAP[" + index + " ]")
        self.definitionCode(target + " = HEAP[int(" + index + ")]")

    #Inserta valor en el heap
    def addSetHeap(self, index:str, value:str):
        #self.code.append("HEAP[" + index + "] = " + value)
        self.definitionCode("HEAP[int(" + index + ")] = " + value)
    
    #Obtiene valor del stack en cierta posicion
    def addGetStack(self,target:str, index:str):
        #self.code.append(target + " = STACK[" + index + "]")
        self.definitionCode(target + " = STACK[int(" + index + ")]")

    #INserta valor al stack
    def addSetStack(self, index:str, value:str):
        #self.code.append("STACK[" + index + "] = " + value)
        self.definitionCode("STACK[int(" + index + ")] = " + value)
    
    def inicioFuncion(self, id):
        if not self.inNatives:
            self.funcionIn = True
        encabezado = "func " + id + "(){\n"
        self.definitionCode(encabezado)

    def finFuncion(self):
        encabezado = "return;\n}\n"
        self.definitionCode(encabezado)
        if not self.inNatives:
            self.funcionIn = False

    def retorno(self):
        self.definitionCode("return;\n")

    #Upper Function
    def addToUpper(self):
        if(self.toUpper):
            return
        self.toUpper = True
        self.inNatives = True

        self.inicioFuncion('to_upper')
        # Label para salir de la funcion
        returnLbl = self.newLabel()
        # Label para la comparacion para buscar fin de cadena
        compareLbl = self.newLabel()

        # Temporal puntero a Stack
        tempP = self.newTemp()

        # Temporal puntero a Heap
        tempH = self.newTemp()

        self.addExpression(tempP, 'P', '1', '+')

        self.addGetStack(tempH, tempP)

        # Temporal para comparark
        tempC = self.newTemp()

        self.addLabel(compareLbl)

        self.addGetHeap(tempC, tempH)

        self.addIf(tempC, '-1', '==', returnLbl)

        temp = self.newTemp()
        pass_label = self.newLabel()
        self.addIf(tempC, '97', '<', pass_label)
        self.addIf(tempC, '122', '>', pass_label)
        self.addExpression(temp, tempC, '32', '-')
        self.addSetHeap(tempH, temp)
        self.addLabel(pass_label)
        self.addExpression(tempH, tempH, '1', '+')

        self.addGoto(compareLbl)

        self.addLabel(returnLbl)
        self.finFuncion()
        self.inNatives = False

    #print str Function
    def addPrintStr(self):
        if(self.printStr):
            return
        self.printStr = True
        self.inNatives = True

        self.inicioFuncion('print_string')
        # Label para salir de la funcion
        returnLbl = self.newLabel()
        # Label para la comparacion para buscar fin de cadena
        compareLbl = self.newLabel()

        # Temporal puntero a Stack
        tempP = self.newTemp()

        # Temporal puntero a Heap
        tempH = self.newTemp()

        self.addExpression(tempP, 'P', '1', '+')

        self.addGetStack(tempH, tempP)

        # Temporal para comparar
        tempC = self.newTemp()

        self.addLabel(compareLbl)

        self.addGetHeap(tempC, tempH)

        self.addIf(tempC, '-1', '==', returnLbl)

        self.definitionCode("fmt.Printf(\"%c\",int(" + tempC + "))")

        self.addExpression(tempH, tempH, '1', '+')

        self.addGoto(compareLbl)

        self.addLabel(returnLbl)
        self.finFuncion()
        self.inNatives = False
    
    #Lower function
    def addToLower(self):
        if(self.toLower):
            return
        self.toLower = True
        self.inNatives = True

        self.inicioFuncion('to_lower')
        # Label para salir de la funcion
        returnLbl = self.newLabel()
        # Label para la comparacion para buscar fin de cadena
        compareLbl = self.newLabel()
        # Temporal puntero a Stack
        tempP = self.newTemp()

        # Temporal puntero a Heap
        tempH = self.newTemp()
        self.addExpression(tempP, 'P', '1', '+')
        self.addGetStack(tempH, tempP)

        # Temporal para comparark
        tempC = self.newTemp()

        self.addLabel(compareLbl)

        self.addGetHeap(tempC, tempH)

        self.addIf(tempC, '-1', '==', returnLbl)

        temp = self.newTemp()
        pass_label = self.newLabel()
        self.addIf(tempC, '65', '<', pass_label)
        self.addIf(tempC, '90', '>', pass_label)
        self.addExpression(temp, tempC, '32', '+')
        self.addSetHeap(tempH, temp)
        self.addLabel(pass_label)
        self.addExpression(tempH, tempH, '1', '+')

        self.addGoto(compareLbl)

        self.addLabel(returnLbl)
        self.finFuncion()
        self.inNatives = False