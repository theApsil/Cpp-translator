from Parser import TreeNode, Node
from Lexer import ErrorTypeSemantic
from SemanticalAnalyzer.ReservedWords import *


class Variable(object):
    def __init__(self, type_v=None, name=None):
        self.type_v = type_v
        self.name = name


class VariableStorage(object):
    def __init__(self):
        self.variables = list()
        self.children = list()
        self.parent = None

    def addChildren(self):
        var_s = VariableStorage()
        self.children.append(var_s)
        var_s.parent = self
        return var_s

    def addVariable(self, var: Variable):
        self.variables.append(var)

    def exist(self, name, scope):
        while scope is not None:
            for value in scope.variables:
                if value.name == name:
                    return True
            scope = scope.parent
        return False

    def localExist(self, name, scope):
        for value in scope.variables:
            if value.name == name:
                return value
        return False

    def getVariable(self, name, scope):
        while scope is not None:
            for value in scope.variables:
                if value.name == name:
                    return value
            scope = scope.parent
        return None


class Function(object):
    def __init__(self, type_v=None, name=None, params=[]):
        self.type_v = type_v
        self.name = name
        self.params = params


class SemanticError:
    def __init__(self, line, name, error_name):
        self.errorName = error_name
        self.line = line
        self.name = name
        self.assumptions = set()

    def addAssumption(self, assumption):
        self.assumptions.add(assumption)

    def __str__(self):
        return "{0} | Error: {1} \"{2}\"" \
            .format(self.line, self.errorName, self.name)


class VariableSemanticAnalyser:
    def __init__(self, tree):
        self.tree = tree
        self.functions = []
        self.file = None

    def findExpressionType(self, node: Node):
        if node.lexeme and node.lexeme.lexemeType.name == 'INT_NUMBER':
            return ['int']
        elif node.lexeme and node.lexeme.lexemeType.name == 'REAL_NUMBER':
            return ['double', 'float']
        elif node.lexeme and node.lexeme.lexemeType.name == 'CHAR_DATA':
            return ['char']
        elif node.lexeme and node.lexeme.lexemeType.name == 'STRING_DATA':
            return ['string']
        else:
            return ['int']

    def addVariable(self, node: Node, scope: VariableStorage):
        newVariable = Variable(None, None)
        typeCheck = None
        errorCheck = None
        for part in node.children:
            if part.rule.name == '<тип данных>':
                newVariable.type_v = part.lexeme.lexeme
            if part.rule.name == '<имя переменной>':
                newVariable.name = part.lexeme.lexeme
            if part.rule.name == '<выражение>':
                if len(part.children) == 0:
                    typeCheck = self.findExpressionType(part)
                else:
                    typeCheck = self.parseExpression(part.children[0], scope)
        if typeCheck and newVariable.type_v not in typeCheck and newVariable.name[0] is not None:
            print(SemanticError(node.lexeme.lineNumber, newVariable.name,
                                ErrorTypeSemantic.TYPE_MISMATCH.value))
            errorCheck = True
        if newVariable.name in ReservedWords.data and newVariable.name[0] is not None:
            print(SemanticError(node.lexeme.lineNumber, newVariable.name,
                                ErrorTypeSemantic.USAGE_OF_RESERVED_IDENTIFIER.value))
            errorCheck = True
        if scope.exist(newVariable.name, scope):
            print(SemanticError(node.lexeme.lineNumber, newVariable.name,
                                ErrorTypeSemantic.MULTIPLE_VARIABLE_DECLARATION.value))
            errorCheck = True
        if errorCheck is None:
            scope.addVariable(newVariable)

    def updateVariableCheck(self, node: Node, scope: VariableStorage):
        typeCheck = None
        nameCheck = ''
        for part in node.children:
            if part.rule.name == '<имя переменной>':
                nameCheck = part.lexeme.lexeme
            if part.rule.name == '<выражение>':
                typeCheck = self.findExpressionType(part)
            if part.rule.name == '<унарный алгебраический оператор>':
                typeCheck = ['int']
        if not scope.exist(nameCheck, scope):
            print(SemanticError(node.lexeme.lineNumber, nameCheck, ErrorTypeSemantic.UNDECLARED_VARIABLE.value))
        else:
            var = scope.getVariable(nameCheck, scope)
            if var.type_v not in typeCheck:
                print(SemanticError(node.lexeme.lineNumber, nameCheck, ErrorTypeSemantic.TYPE_MISMATCH.value))

    def addFunction(self, node: Node, scope: VariableStorage):
        newFunction = Function()
        for part in node.children:
            if part.rule.name == '<тип данных>':
                newFunction.type_v = part.lexeme.lexeme
            if part.rule.name == '<имя переменной>':
                newFunction.name = part.lexeme.lexeme
            if part.rule.name == '<формальные параметры>':
                children = part.children
                while len(children) != 2:
                    var = Variable(children[0].lexeme.lexeme, children[1].lexeme.lexeme)
                    scope.addVariable(var)
                    newFunction.params.append(var)
                    children = children[2].children
                var = Variable(children[0].lexeme.lexeme, children[1].lexeme.lexeme)
                scope.addVariable(var)
                newFunction.params.append(var)
            if part.rule.name == '<тело функции>':
                self.parse(part, scope)
                returnExpression = part.children
                while len(returnExpression) != 1:
                    returnExpression = returnExpression[1].children
                returnExpression = self.parseExpression(returnExpression[0].children[0].children[0], scope)
                if newFunction.type_v in returnExpression:
                    self.functions.append(newFunction)
                elif len(returnExpression) == 0:
                    print(SemanticError(node.lexeme.lineNumber, '', ErrorTypeSemantic.EXPRESSION_MULTIPLE_TYPES.value))
                else:
                    print(SemanticError(node.lexeme.lineNumber, newFunction.type_v + '!=' + str(returnExpression[0]),
                                        ErrorTypeSemantic.FUNCTION_TYPE_MISMATCH.value))

    def parseExpression(self, expression, scope: VariableStorage):
        if expression.rule.name == '<алгебраическое выражение>':
            if len(expression.children) == 1:
                return [self.parseOperand(expression.children[0], scope)]
            elif expression.children[0].rule.name == '<унарный алгебраический оператор>':
                return [self.parseOperand(expression.children[1], scope)]
            elif expression.children[1].rule.name == '<унарный алгебраический оператор>':
                return [self.parseOperand(expression.children[0], scope)]
            else:
                exp_type = self.parseOperand(expression.children[0], scope)
                expression_temp = expression.children[2]
                while len(expression_temp.children) == 3:
                    if exp_type != self.parseOperand(expression_temp.children[0], scope):
                        exp_type = None
                    expression_temp = expression_temp.children[2]
                if exp_type != self.parseOperand(expression_temp.children[0], scope):
                    exp_type = None
                return [exp_type]
        if expression.rule.name == '<булево выражение>':
            if expression.children[0].children[0].children[0].rule.name == '<имя переменной>' and len(
                    expression.children[0].children) == 1:
                return [scope.getVariable(expression.children[0].children[0].children[0].lexeme.lexeme,
                                          scope).type_v]
            if 'целое число' in expression.children[0].children[0].children[0].children[0].rule.name and len(
                    expression.children[0].children) == 1:
                return ['int']
            if 'вещественное число' in expression.children[0].children[0].children[0].children[0].rule.name and len(
                    expression.children[0].children) == 1:
                return ['float', 'double']
            if expression.children[0].children[0].children[0].rule.name == '<вызов функции>' and len(
                    expression.children[0].children) == 1:
                for func in self.functions:
                    if func.name == expression.children[0].children[0].children[0].children[0].lexeme.lexeme:
                        return [func.type_v]
            else:
                return ['bool']

    def parseOperand(self, operand: TreeNode, scope: VariableStorage):
        if operand.children[0].rule.name == '<имя переменной>':
            if scope.getVariable(operand.children[0].lexeme.lexeme, scope):
                return scope.getVariable(operand.children[0].lexeme.lexeme, scope).type_v
            else:
                print(SemanticError(operand.lexeme.lineNumber, operand.lexeme.lexeme,
                                    ErrorTypeSemantic.UNDECLARED_VARIABLE.value))
                return None
        elif operand.children[0].rule.name == '<вызов функции>':
            for func in self.functions:
                if func.name == operand.children[0].children[0].lexeme.lexeme:
                    temp = operand.children[0]
                    if len(operand.children[0].children) == 2:
                        temp = operand.children[0].children[1]
                    params = []
                    while len(temp.children) == 2:
                        if len(temp.children[0].children) != 0:
                            params += self.parseExpression(temp.children[0].children[0], scope)
                        else:
                            params += self.findExpressionType(temp.children[0])
                        temp = temp.children[1]
                    if len(operand.children[0].children) == 2:
                        params += self.findExpressionType(temp.children[0])
                    if len(params) != len(func.params):
                        print(SemanticError(operand.lexeme.lineNumber, func.name,
                                            ErrorTypeSemantic.FUNCTION_PARAMETERS_MISMATCH.value))
                        return None
                    else:
                        for i in range(len(params)):
                            if params[i] != func.params[i].type_v:
                                print(SemanticError(operand.lexeme.lineNumber, func.name,
                                                    ErrorTypeSemantic.FUNCTION_PARAMETERS_MISMATCH.value))
                                return None
                        return func.type_v
            print(SemanticError(operand.lexeme.lineNumber, operand.children[0].children[0].lexeme.lexeme,
                                ErrorTypeSemantic.UNDECLARED_FUNCTION.value))
            return None
        else:
            return 'int'

    def parse(self, node, scope: VariableStorage):
        newScope = scope
        if node.rule.name == '<инициализация переменной>':
            self.addVariable(node, scope)
        if node.rule.name == '<обновление переменной>':
            self.updateVariableCheck(node, scope)
        if node.rule.name == '<цикл for>':
            newScope = scope.addChildren()
        if node.rule.name == '<цикл while>':
            newScope = scope.addChildren()
        if node.rule.name == '<главная функция>':
            newScope = scope.addChildren()
        if node.children:
            for nextNode in node.children:
                if nextNode.rule.name == '<объявление функции>':
                    newScope = scope.addChildren()
                    self.addFunction(nextNode, newScope)
                else:
                    self.parse(nextNode, newScope)