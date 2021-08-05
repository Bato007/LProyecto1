import re
import itertools

# Extrae los valores individuales de la clausula
def getVariables(expressions):
    global literals
    literals = []
    for expression in expressions:
        for element in expression:
            for literal in element:
                if (literal != '~') and (literal not in literals) and (literal != '{') and (literal != '}') and (literal != ','):
                    literals.append(literal)


# Recibo {{p},{~p}} -> retorno p∧~p
def obtenerFormulaBooleana(clausula):
    
    getVariables(clausula)
    # Remuevo el primer y ultimo string -> {p},{~p}
    clausula = clausula[1:-1]
    subconjuntos = re.findall('\{(.*?)\}', clausula)

    # Junto con parentesis
    res = ""
    for subconjunto in subconjuntos:
        # Reemplazo los and
        subconjunto = subconjunto.replace(',', '∨')
        # Coloco los parentesis
        res += "("+subconjunto+")"

    # Reemplazo los or
    res = res.replace(")(", ")∧(")
    # Retorno el resultado en forma booleana
    return res



    
# Recibo operacion booleana y retorno el resultado correspondiente
# ej p∧~p -> 1 ∧ ~0 = 1
def calcularAsignacion(operacionBooleana):
    # Por parentesis en la expresion booleana
    expresiones = re.findall('\((.*?)\)', operacionBooleana)

    orExpresions = []
    
    for i in range(2**len(literals)): # Genera las combinaciones de literales
        
        litVars = {}
        orExpresions = []
        binary = bin(i)
        binary = binary.replace('b','')
        binary = binary.zfill(len(literals))
        binary = str(binary[len(binary)-len(literals):len(binary)]) # Combinacion concurrente
        
        for expresion in expresiones:
            # Reemplazo el abecedario por un valor 0 o 1
            for literal in literals:
                # Intercambia los valores de la expresion por los generados en binario
                expresion = expresion.replace(literal, binary[literals.index(literal)])
                litVars[literal] = binary[literals.index(literal)]
                
            # Verifico si hay un negativo
            if ("~" in expresion):
                i = expresion.index('~')
                # Se reemplaza por el valor contrario
                if (expresion[i+1] == '0'):
                    expresion = expresion[0:i+1] + "1" + expresion[i+2:]
                else:
                    expresion = expresion[0:i+1] + "0" + expresion[i+2:]
                # Se remueve el negativo
                expresion = expresion.replace('~', '')
            
            # Evaluo los and
            valores = expresion.split('∨')
            if (len(valores) > 1):
                resultadoAnd = recEvaluarAnd(valores)  
                # Agrego aL resultado del or
                orExpresions.append(resultadoAnd)
            else:
                # Agrego aL resultado del or
                orExpresions.append(expresion)
        
        # Evaluo los or
        if (len(orExpresions) > 1):
            resultadoFinal = recEvaluarOr(orExpresions)
            print("Resultado de la expresion", operacionBooleana, "evaluada en ",litVars, "es ", resultadoFinal)
        else:
            print("Resultado de la expresion", operacionBooleana, "evaluada en ",litVars, "es ", orExpresions[0])
        


def recEvaluarAnd(valores):
    andOperator = {('0', '0'): '0', ('0', '1'): '0', ('1', '0'): '0', ('1','1'): '1'}

    [a, b] = valores[0], valores[1]
    # Obtengo la salida de evaular a, b en un and
    salida = andOperator[tuple([a, b])]

    # Reemplazo valores
    valoresActuales = valores[1:]
    if (len(valoresActuales) > 1):
        valoresActuales[0] = salida
        recEvaluarAnd(valoresActuales)
         
    return salida

def recEvaluarOr(valores):
    orOperator = {('0', '0'): '0', ('0', '1'): '1', ('1', '0'): '1', ('1','1'): '1'}

    [a, b] = valores[0], valores[1]
    # Obtengo la salida de evaular a, b en un or
    salida = orOperator[tuple([a, b])]

    # Reemplazo valores
    valoresActuales = valores[1:]
    if (len(valoresActuales) > 1):
        valoresActuales[0] = salida
        recEvaluarOr(valoresActuales)
    
    return salida

operacionBooleana = obtenerFormulaBooleana('{{p,r,~s},{q,p,s}}')
examples = [
    [['p'], ['~p']],
    [['q', 'p', '~p']],
    [['~p', '~r', '~s'], ['~q', '~p', '~s']],
    [['~p', '~q'], ['q', '~s'], ['~p', 's'], ['~q', 's']],
    [['~p', '~q', '~r'], ['q', '~r', 'p'], ['~p', 'q', '~r']],
    [['r'], ['~q', '~r'], ['~p', 'q', '~r'], ['q']]
]
examplesFormaClausula = [
    '{{p},{~p}}',
    '{{q,p,~p}}',
    '{{~p,~r,~s}},{~q,~p,~s}}',
    '{{~p,~q},{q,~s},{~p,s},{~q,s}}',
    '{{~p,~q,~r},{q,~r,p},{~p,q,~r}}',
    '{{r,~q,~r},{~p,q,~r},{q}}'
]
######################################################################
print('____________________________________________')
print('EJEMPLOS DENTRO DEL PROGRAMA')
print('____________________________________________')
for i in range(len(examples)):
    print(i+1, examples[i])
elegido = int(input('\nElija el numero de la operacion a evaluar: '))

print('____________________________________________')
operacionBooleana = obtenerFormulaBooleana(examplesFormaClausula[elegido-1])
calcularAsignacion(operacionBooleana)