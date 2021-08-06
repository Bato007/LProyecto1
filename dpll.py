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
  elements = []
  B1 = []
  for i in B:
    B1.append(i[:])
  for element in B1:
    if literal in element:
      elements.append(element)  # Se agregan los que se quieren volar !q
  for element in elements:
      B1.remove(element)
  # Ahora se eliminan las literales
  comp = literal[1] if literal[0] == '~' else ('~' + literal)
  for element in B1:
    if comp in element:
      element.remove(comp)
  return B1[:]


def DPLL(B, I):
    # Casos bases
    if len(B) == 0:
        return True, I
    for element in B:
        if len(element) == 0:
            return False, {}
    literal = selectLiteral(I)

    B1 = cleanLiteral(B, literal)  # 2
    Iaux = I.copy()
    Iaux[literal] = 1              # Hacer true L
    result, I1 = DPLL(B1, Iaux)
    if result:
        return True, I1.copy()

    B2 = cleanLiteral(B, '~' + literal)
    Iaux = I.copy()
    Iaux[literal] = 0
    result, I2 = DPLL(B2, Iaux)
    if result:
        return True, I2.copy()

    return False, {}


examples = [
    [['p'], ['~p']],
    [['q', 'p', '~p']],
    [['~p', '~r', '~s'], ['~q', '~p', '~s']],
    [['~p', '~q'], ['q', '~s'], ['~p', 's'], ['~q', 's']],
    [['~p', '~q', '~r'], ['q', '~r', 'p'], ['~p', 'q', '~r']],
    [['r'], ['~q', '~r'], ['~p', 'q', '~r'], ['q']]
]

for i in examples:
  getVariables(i)
  print('Respuesta:', DPLL(i, {}))
