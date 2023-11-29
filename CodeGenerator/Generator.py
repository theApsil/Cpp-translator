INDENT = " " * 4
Types = {
    'bool': 'boolean',
    'char': 'char',
    'short': 'smallint',
    'unsigned short int': 'word',
    'int': 'integer',
    'short int': 'smallint',
    'unsigned short': 'word',
    'unsigned int': 'longword',
    'float': 'real',
    'double': 'double',
}


class GeneratorNode(object):
    def __init__(self, parent, name=None, body=None):
        self.parent = parent
        self.name = name
        self.body = body

    def __setBody(self, body: []):
        self.body = body

    def __appendNode(self, node):
        if self.body is None:
            self.body = [node]
        else:
            self.body.append(node)

    def addBody(self, body):
        if isinstance(body, list):
            self.__setBody(body)
        else:
            self.__appendNode(body)


class VarNode(GeneratorNode):
    def __init__(self, parent, name, varType=None, body=None):
        super().__init__(parent, name, body)
        self.varType = varType

    def __repr__(self):
        result = ''
        if self.varType is not None:
            result += f'{self.varType} '

        result += f'{self.name}'
        bodyStr = ''
        if self.body is not None:
            bodyStr += ' = '
            for item in self.body:
                bodyStr += str(item)

        return result + bodyStr


class FuncNode(GeneratorNode):
    def __init__(self, parent, name, body=None, params=None, returnType=None):
        super().__init__(parent, name, body)
        self.returnType = returnType
        self.params = params
        self.vars = []

    def __repr__(self):
        result = ''

        if self.returnType is not None:
            result += f'{self.returnType} '

        result += self.name

        paramsStr = ''
        if len(self.params) > 0:
            for param in self.params:
                paramsStr += str(param) + ','

        result += f'({paramsStr[:-1]})'

        return result

    def __str__(self):
        result = ''

        if self.returnType is not None:
            result += f'{self.returnType} '

        result += self.name

        paramsStr = ''
        if self.params is not None:
            for param in self.params:
                paramsStr += str(param) + ','

        result += f'({paramsStr[:-1]})'

        return result

    def addVar(self, var: VarNode):
        self.vars.append(var)


class ExpressionNode(GeneratorNode):
    def __init__(self, parent):
        super().__init__(parent)

    def __repr__(self):
        result = ''
        for item in self.body:
            result += str(item)

        return result

    def __str__(self):
        result = ''
        for item in self.body:
            result += str(item)

        return result


class IfNode(GeneratorNode):
    def __init__(self, parent, boolExpr):
        super().__init__(parent)
        self.boolExp = boolExpr


class ElseNode(GeneratorNode):
    def __init__(self, parent):
        super().__init__(parent)


class ForNode(GeneratorNode):
    def __init__(self, parent, firstExpr, secondExpr, thirdExpr, body):
        super().__init__(parent, body=body)
        self.firstExpr = firstExpr
        self.secondExpr = secondExpr
        self.thirdExpr = thirdExpr


class ReturnNode(GeneratorNode):
    def __init__(self, parent):
        super().__init__(parent, 'return')


class Generator(object):
    def __init__(self, tree):
        if tree.rule.name != 'GAMMA':
            raise ValueError
        self.tree = tree.children[0]
        self.resultTree = FuncNode(None, 'GAMMA')
        self.resultCode = None

    def __getNearestFunc(self, startNode: GeneratorNode):
        result = startNode

        while not isinstance(result, FuncNode) or result.name != 'GAMMA':
            if result.name != 'main':
                return result
            result = result.parent

        return result

    def __parseFunc(self, treeNode, parentNode):
        returnType = treeNode.children[0].lexeme.lexeme
        funcName = treeNode.children[1].lexeme.lexeme
        params = self.__parseFormalParams(treeNode.children[2], parentNode)
        result = FuncNode(parentNode, funcName, params=params if len(params) > 0 else None, returnType=returnType)
        body = self.__parse(treeNode.children[3], result)
        result.addBody(body)
        return result

    def __parseFunCall(self, treeNode, parentNode):
        funName = treeNode.children[0].lexeme.lexeme
        funParams = None
        if len(treeNode.children) > 1:
            funParams = self.__parseFactParams(treeNode.children[1], parentNode)
        return FuncNode(parentNode, funName, params=funParams)

    def __parseFormalParams(self, treeNode, parentNode):
        result = [VarNode(parentNode, treeNode.children[1].lexeme.lexeme, varType=treeNode.children[0].lexeme.lexeme)]

        if len(treeNode.children) == 3:
            result += self.__parseFormalParams(treeNode.children[2], parentNode)

        return result

    def __parseFactParams(self, treeNode, parentNode):
        result = []
        for child in treeNode.children:
            if child.rule.name == '<выражение>':
                expression = ExpressionNode(parentNode)
                self.__parseExpression(child, expression, parentNode)
                result.append(expression)
            else:
                result += self.__parseFactParams(child, parentNode)

        return result

    def __parseMain(self, treeNode, parentNode):
        result = FuncNode(parentNode, 'main', returnType='int')
        result.addBody(self.__parse(treeNode.children[0], result))
        return result

    def __parseVar(self, treeNode, parentNode):
        if treeNode.rule.name == '<обновление переменной>':
            return self.__parseUpdateVar(treeNode, parentNode)
        elif treeNode.rule.name == '<инициализация переменной>' or treeNode.rule.name == '<новая переменная>':
            return self.__parseInitVar(treeNode, parentNode)

        return None

    def __parseUpdateVar(self, treeNode, parentNode):
        if treeNode.children[0].rule.name == '<унарный алгебраический оператор>':
            varName = treeNode.children[1].lexeme.lexeme
            operator = treeNode.children[0].lexeme.lexeme
            if operator == '++':
                result = ExpressionNode(parentNode)
                result.addBody(['Inc', '(', varName, ')'])
            else:
                result = ExpressionNode(parentNode)
                result.addBody(['Dec', '(', varName, ')'])
        else:
            varName = treeNode.children[0].lexeme.lexeme
            if treeNode.children[1].rule.name == '<унарный алгебраический оператор>':
                operator = treeNode.children[1].lexeme.lexeme
                if operator == '++':
                    result = ExpressionNode(parentNode)
                    result.addBody(['Inc', '(', varName, ')'])
                else:
                    result = ExpressionNode(parentNode)
                    result.addBody(['Dec', '(', varName, ')'])
            else:
                expVal = ExpressionNode(parentNode)
                self.__parseExpression(treeNode.children[1], expVal, parentNode)
                result = VarNode(parentNode, varName)
                result.addBody(expVal)

        return result

    def __parseInitVar(self, treeNode, parentNode):
        varType = treeNode.children[0].lexeme.lexeme
        varName = treeNode.children[1].lexeme.lexeme
        expVal = ExpressionNode(parentNode)
        if len(treeNode.children) > 2:
            self.__parseExpression(treeNode.children[2], expVal, parentNode)

        result = VarNode(parentNode, varName, varType)

        if expVal.body is not None:
            result.addBody(expVal)

        func = self.__getNearestFunc(parentNode)
        func.addVar(result)

        return result

    def __parseFor(self, treeNode, parentNode):
        firstExp = self.__parse(treeNode.children[0].children[0], parentNode)
        secondExp = self.__parse(treeNode.children[1], parentNode)
        thirdExp = self.__parse(treeNode.children[2], parentNode)
        body = self.__parse(treeNode.children[3], parentNode)

        return ForNode(parentNode, firstExp, secondExp, thirdExp, body)

    def __parseIf(self, treeNode, parentNode):
        result = IfNode(parentNode, self.__parse(treeNode.children[0], parentNode))
        body = self.__parse(treeNode.children[1], parentNode)
        result.addBody(body)

        return result

    def __parseElse(self, treeNode, parentNode):
        result = ElseNode(parentNode)
        result.addBody(self.__parse(treeNode.children[0], parentNode))

        return result

    def __parseWhile(self, treeNode, parentNode):
        boolExpr = self.__parse(treeNode.children[0], parentNode)
        body = self.__parse(treeNode.children[1], parentNode)
        result = ForNode(parentNode, None, boolExpr, None, body)

        return result

    def __parseReturn(self, treeNode, parentNode):
        result = ReturnNode(parentNode)

        if treeNode.rule.name == '<выход>':
            return result

        expr = ExpressionNode(parentNode)
        self.__parseExpression(treeNode.children[0], expr, parentNode)
        result.addBody(expr)

        return result

    def __parseExpression(self, treeNode, exprNode: ExpressionNode, parentNode):
        if treeNode.rule.name == '<вызов функции>':
            exprNode.addBody(self.__parseFunCall(treeNode, parentNode))
            return
        elif treeNode.rule.name == '<имя переменной>' or \
                treeNode.rule.name == '<число>' or \
                treeNode.rule.name == '<бинарный алгебраический оператор>' or \
                treeNode.rule.name == '<булева константа>' or \
                treeNode.rule.name == '<оператор сравнения>' or \
                treeNode.rule.name == '<выражение>' and len(treeNode.children) == 0:
            exprNode.addBody(treeNode.lexeme.lexeme)
            return

        for child in treeNode.children:
            self.__parseExpression(child, exprNode, parentNode)

    def __parse(self, treeNode, parentNode):
        if treeNode.rule.name == '<главная функция>':
            return self.__parseMain(treeNode, parentNode)
        elif treeNode.rule.name == '<цикл for>':
            return self.__parseFor(treeNode, parentNode)
        elif treeNode.rule.name == '<цикл while>':
            return self.__parseWhile(treeNode, parentNode)
        elif treeNode.rule.name == '<обновление переменной>' or \
                treeNode.rule.name == '<инициализация переменной>' or \
                treeNode.rule.name == '<новая переменная>':
            return self.__parseVar(treeNode, parentNode)
        elif treeNode.rule.name == '<объявление функции>':
            return self.__parseFunc(treeNode, parentNode)
        elif treeNode.rule.name == '<выражение>' or treeNode.rule.name == '<булево выражение>':
            expression = ExpressionNode(parentNode)
            self.__parseExpression(treeNode, expression, parentNode)
            return expression
        elif treeNode.rule.name == '<возврат значения>' or treeNode.rule.name == '<выход>':
            return self.__parseReturn(treeNode, parentNode)
        elif treeNode.rule.name == '<условие>':
            return self.__parseIf(treeNode, parentNode)
        elif treeNode.rule.name == '<иначе>':
            return self.__parseElse(treeNode, parentNode)
        else:
            result = []
            for child in treeNode.children:
                tempRes = self.__parse(child, parentNode)
                if tempRes is not None:
                    if isinstance(tempRes, VarNode) and isinstance(parentNode, ForNode) or \
                            isinstance(tempRes, VarNode) and tempRes.varType is None or \
                            not isinstance(tempRes, VarNode):
                        if isinstance(tempRes, list):
                            result += tempRes
                        else:
                            result.append(tempRes)

            return result

    def __generateVar(self, node, level):
        result = INDENT * level

        result += node.name

        if node.varType is not None:
            result += ' : ' + Types[node.varType]

        if node.body is not None:
            result += ' := '
            for item in node.body:
                result += str(item)

        return result

    def __generateIf(self, node: IfNode, level):
        result = INDENT * level + 'if ('
        result += str(node.boolExp) + ') then\n'
        result += INDENT * level + 'begin\n'
        for item in node.body:
            result += self.__generateCode_Helper(item, level + 1)
        result += INDENT * level + 'end\n'

        return result

    def __generateElse(self, node: ElseNode, level):
        result = INDENT * level + 'else\n'
        result += INDENT * level + 'begin\n'
        for item in node.body:
            result += self.__generateCode_Helper(item, level + 1)
        result += INDENT * level + 'end\n'

        return result


    def __generateFor(self, node, level):
        result = INDENT * level + 'while (' + str(node.secondExpr) + ') do\n'

        for item in node.body:
            result += self.__generateCode_Helper(item, level + 1)

        if node.thirdExpr is not None:
            result += INDENT * (level + 1) + str(node.thirdExpr) + ';\n\n'

        return result

    def __generateVarsBlock(self, varsList, level):
        if len(varsList) == 0:
            return ''

        result = INDENT * level + 'var\n'
        for var in varsList:
            result += self.__generateVar(var, level + 1) + ';\n'

        return result

    def __generateFunc(self, node, level):
        result = INDENT * level

        if node.name == 'main':
            result += 'begin\n'

            for item in node.body:
                result += self.__generateCode_Helper(item, level + 1)

            result += 'end.\n'
            return result

        if node.returnType is None:
            result += 'procedure '
        else:
            result += 'function '

        result += node.name

        paramsStr = ''
        if node.params is not None:
            for param in node.params:
                paramsStr += self.__generateVar(param, 0) + ','
        paramsStr = paramsStr[:-1]
        result += f'({paramsStr})'

        if node.returnType is not None:
            result += f': {Types[node.returnType]}\n'
        else:
            result += '\n'

        result += self.__generateVarsBlock(node.vars, level)
        result += INDENT * level + 'begin\n'

        for item in node.body:
            result += self.__generateCode_Helper(item, level + 1)

        result += 'end;\n\n'

        return result

    def __generateCode_Helper(self, node, level=0):
        result = INDENT * level

        if isinstance(node, FuncNode):
            return self.__generateFunc(node, level)
        elif isinstance(node, VarNode):
            return self.__generateVar(node, level) + ';\n'
        elif isinstance(node, ForNode):
            return self.__generateFor(node, level)
        elif isinstance(node, FuncNode):
            return
        elif isinstance(node, IfNode):
            return self.__generateIf(node, level)
        elif isinstance(node, ElseNode):
            return self.__generateElse(node, level)
        elif isinstance(node, ReturnNode):
            if node.body is not None:
                result += 'Result := '
                for item in node.body:
                    result += str(item)
            else:
                result += 'exit'

            return result + ';\n'

        return result

    def __generateCode(self):
        if self.resultTree.name != 'GAMMA':
            raise ValueError

        result = self.__generateVarsBlock(self.resultTree.vars, 0)

        for item in self.resultTree.body:
            result += self.__generateCode_Helper(item)

        return result

    def generate(self):
        self.resultTree.addBody(self.__parse(self.tree, self.resultTree))
        self.resultCode = self.__generateCode()