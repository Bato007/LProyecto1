import re

# Donde la llave es el valor retornado y el 
# valor son los valores evaluados para obtener la llave
andOperator = {'0': [[0, 0], [0, 1], [1, 0]], '1': [[1,1]]}
orOperator = {'0': [[0, 0]], '1': [[0, 1], [1, 0], [1,1]]}
notOperator = {'0': [[1]], '1': [[0]]}

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

    for expresion in expresiones:
        # Reemplazo el abecedario por un valor 0 o 1
        expresion = expresion.replace('p', '0')
        expresion = expresion.replace('q', '0')
        expresion = expresion.replace('r', '0')
        expresion = expresion.replace('s', '0')

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

        print(expresion)


operacionBooleana = obtenerFormulaBooleana('{{p,r,~s},{q,p,s}}')
calcularAsignacion(operacionBooleana)
