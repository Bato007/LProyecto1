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


def DPLL(B, I):
    # Casos bases
    if len(B) == 0:
        return True, I
    for element in B:
        if len(element) == 0:
            return False, {}
    literal = selectLiteral(I)

    B1 = cleanLiteral(B, literal)  # 2
    I[literal] = 1                # Hacer true L
    result, I1 = DPLL(B1, I)
    if result:
        return True, I1

    B2 = cleanLiteral(B, '~' + literal)
    I[literal] = 0
    result, I2 = DPLL(B2, I)
    if result:
        return True, I2

    return False, {}


temp = [['q', 'p', '~p'], ['q']]
getVariables(temp)
print(literals)
print(selectLiteral({}))
print(selectLiteral({'q': 0}))
