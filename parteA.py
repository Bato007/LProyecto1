import re


# Recibo {{p},{~p}} -> retorno p∧~p
def obtenerFormulaBooleana(clausula):
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

    for expresion in expresiones:
        # Reemplazo el abecedario por un valor 0 o 1
        expresion = expresion.replace('p', '1')
        expresion = expresion.replace('q', '1')
        expresion = expresion.replace('r', '1')
        expresion = expresion.replace('s', '1')

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
        resultadoAnd = recEvaluarAnd(valores)
        # Agrego aL resultado del or
        orExpresions.append(resultadoAnd)

    # Evaluo los or
    resultadoFinal = recEvaluarOr(orExpresions)
    print("Resultado de la expresion", operacionBooleana, "evaluada todo en 1 es", resultadoFinal)
    return resultadoFinal


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
calcularAsignacion(operacionBooleana)
