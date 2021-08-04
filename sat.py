def getVariables(expressions):
    global literals
    literals = []
    for expression in expressions:
        for element in expression:
            for literal in element:
                if (literal != '~') and (literal not in literals):
                    literals.append(literal)


def selectLiteral(I):   # Se encarga de obtener las lilterales
    keys = list(I.keys())

    # Ahora devolvemos otra literal
    for literal in literals:
        if literal not in keys:
            return literal

def cleanLiteral(B, literal):
    B_copy = B.copy()
    neg = '~' + str(literal)
    flag = 0
    sign = ''
    for i in B_copy:
        if literal in i:
            B.remove(i)
            flag += 1
            sign = 1

    if flag == 0:
        for i in B_copy:
            if neg in i:
                B.remove(i)
                sign = 0

    elif flag != 0:
        for i in B:
            if (neg in i) and (len(B[B.index(i)]) > 1):
                B[B.index(i)].remove(neg)
            elif (neg in i) and (len(B) == 1):
                B[B.index(i)].remove(neg)


    return B, sign
"""
        elif (neg in i) and (len(B[B.index(i)]) == 1):
            B.remove(i)
            sign = 0
"""
    

def DPLL(B, I):
    # Casos bases
    if len(B) == 0:
        return True, I
    for element in B:
        if len(element) == 0:
            return False, {}

    literal = selectLiteral(I)
    print(literal)
    print(B)
    B1, sign = cleanLiteral(B, literal)  # 2
    I[literal] = sign                # Hacer true L
    result, I1 = DPLL(B1, I)
    if result:
        return True, I1

    """
    B2 = cleanLiteral(B, '~' + literal)
    I[literal] = 0
    result, I2 = DPLL(B2, I)
    if result:
        return True, I2
    """
    return False, {}


temp = [['r'],['~q','~r'],['~p','q','~r'],['q']]
temp1 = [['~p','~r','~s'],['~q','~p','~s']]
temp2 = [['p'],['~p']]
I = {}

getVariables(temp1)
print(literals)
"""
print(literals)
print(selectLiteral({}))
print(selectLiteral({'q': 0}))
"""
print(DPLL(temp2,I))