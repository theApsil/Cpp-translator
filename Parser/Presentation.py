import re
from Lexer import LexemeType
from Lexer import LexicalAnalyzer

VERTICAL_SYMBOL = "│"
VERTICAL_FORK = "├"
HORIZONTAL_SYMBOL = "─"
LEFT_SYMBOL = "└"
LEVEL_INDENT = 2

GAMMA_RULE = u"GAMMA"


class TreeNode(object):
    def __init__(self, rule, lexeme):
        self.rule = rule
        self.lexeme = lexeme
        self.children = []

    def __repr__(self):
        return str(self.rule)

    def addChild(self, child):
        self.children = [child] + self.children


class Production(object):
    def __init__(self, *terms):
        self.terms = terms

    def __len__(self):
        return len(self.terms)

    def __getitem__(self, index):
        return self.terms[index]

    def __iter__(self):
        return iter(self.terms)

    def __repr__(self):
        return " ".join(str(t) for t in self.terms)

    def __eq__(self, other):
        if not isinstance(other, Production):
            return False
        return self.terms == other.terms

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.terms)

    def add(self, term):
        self.terms += (term,)


class Rule(object):
    def __init__(self, name, *productions: Production):
        self.name = name
        self.productions = list(productions)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s -> %s" % (self.name, " | ".join(repr(p) for p in self.productions))

    def add(self, *productions):
        self.productions.extend(productions)


class RegexpRule(object):
    def __init__(self, regexp):
        self.regexp = regexp

    def __repr__(self):
        return self.regexp

    def __str__(self):
        return self.regexp


class State(object):
    def __init__(self, name, production, dotIndex, startColumn):
        self.name = name
        self.production = production
        self.startColumn = startColumn
        self.end_column = None
        self.dotIndex = dotIndex
        self.rules = [t for t in production if isinstance(t, Rule)]
        self.children = []

    def __repr__(self):
        terms = [str(p) for p in self.production]
        terms.insert(self.dotIndex, u"·")
        return "%-5s -> %-16s [%s-%s]" % (self.name, " ".join(terms), self.startColumn, self.end_column)

    def __eq__(self, other):
        return (self.name, self.production, self.dotIndex, self.startColumn) == \
            (other.name, other.production, other.dotIndex, other.startColumn)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.name, self.production))

    def __len__(self):
        return len(str(self))

    def completed(self):
        return self.dotIndex >= len(self.production)

    def next_term(self):
        if self.completed():
            return None
        return self.production[self.dotIndex]

    def addChild(self, state):
        self.children.append(state)


class Column(object):
    def __init__(self, index, token):
        self.index = index
        self.token = token
        self.states = []
        self._unique = set()

    def __str__(self):
        return str(self.index)

    def __len__(self):
        return len(self.states)

    def __iter__(self):
        return iter(self.states)

    def __getitem__(self, index):
        return self.states[index]

    def enumfrom(self, index):
        for i in range(index, len(self.states)):
            yield i, self.states[i]

    def add(self, state):
        if state not in self._unique:
            self._unique.add(state)
            state.end_column = self
            self.states.append(state)
            return True
        return False

    def print_(self, completedOnly=False):
        print("[%s] %r" % (self.index, self.token))
        print("=" * 35)
        for s in self.states:
            if completedOnly and not s.completed():
                continue
            print(repr(s))
        print()


class Node(object):
    def __init__(self, value, children, lexeme):
        self.state = value
        self.children = children
        self.lexeme = lexeme

    def __repr__(self):
        terms = [str(p) for p in self.state.production]
        terms.insert(self.state.dotIndex, u"·")
        return "{0} -> {1}         Lexeme: {2}".format(self.state.name, " ".join(terms), self.lexeme)


class Earley:
    class SemanticError:
        def __init__(self, token):
            self.token = token
            self.assumptions = set()

        def addAssumption(self, assumption):
            self.assumptions.add(assumption)

        def __str__(self):
            return "{0} | Error: expected {1} instead of \"{2}\"" \
                .format(self.token.lineNumber, " or ".join(map(lambda x: "\'" + str(x) + "\'", self.assumptions)),
                        self.token.lexeme)

    def __init__(self, rules, axiom):
        self.rules = rules
        self.axiom = None
        self.table = None
        self.semanticError = None

        for rule in rules:
            if rule.name == axiom:
                self.axiom = rule

        if self.axiom is None:
            raise ValueError("Invalid axiom")

    def isOk(self):
        return self.semanticError is not None

    def findErrors(self):
        lastNonEmptyCol = None
        lastNonEmptyColNumber = None
        for i, col in enumerate(self.table[::-1]):
            if col:
                lastNonEmptyCol = col
                lastNonEmptyColNumber = len(self.table) - i - 1
                break

        if lastNonEmptyColNumber == len(self.table) - 1:
            self.semanticError = self.SemanticError(
                LexicalAnalyzer.LexemeArrayType("END OF FILE", LexemeType.EOF, lastNonEmptyCol.token.lineNumber))
        else:
            self.semanticError = self.SemanticError(self.table[lastNonEmptyColNumber + 1].token)

        for st in lastNonEmptyCol:
            if not st.completed() and not isinstance(st.production[st.dotIndex], Rule):
                self.semanticError.addAssumption(st.production[st.dotIndex])

    def __predict(self, col, rule, state):
        for prod in rule.productions:
            newState = State(rule.name, prod, 0, col)
            col.add(newState)
            state.addChild(newState)

    def __scan(self, col, state, token):
        if not isinstance(token, RegexpRule):
            if token == col.token.lexeme:
                col.add(State(state.name, state.production, state.dotIndex + 1, state.startColumn))
                state.addChild(col[-1])
        else:
            match = re.search(token.regexp, col.token.lexeme)
            if match:
                col.add(State(state.name, state.production, state.dotIndex + 1, state.startColumn))
                state.addChild(col[-1])

    def __complete(self, col, state):
        if not state.completed():
            return
        for st in state.startColumn:
            term = st.next_term()
            if not isinstance(term, Rule):
                continue
            if term.name == state.name:
                col.add(State(st.name, st.production, st.dotIndex + 1, st.startColumn))
                st.addChild(col[-1])

    def parse(self, lexemeArray):
        self.table = [Column(i, tok) for i, tok in enumerate([None] + lexemeArray)]
        self.table[0].add(State(GAMMA_RULE, Production(self.axiom), 0, self.table[0]))

        for i, col in enumerate(self.table):
            for state in col:
                if state.completed():
                    self.__complete(col, state)
                else:
                    term = state.next_term()
                    if isinstance(term, Rule):
                        self.__predict(col, term, state)
                    elif i + 1 < len(self.table):
                        self.__scan(self.table[i + 1], state, term)

            # col.print_(completedOnly = True)

        # find gamma rule in last table column (otherwise fail)
        for st in self.table[-1]:
            if st.name == GAMMA_RULE and st.completed():
                return True
        else:
            self.findErrors()
            return False

    def printError(self):
        if self.semanticError is None:
            pass  # позырить
        else:
            print(self.semanticError)

    def printTableToFile(self, tableType="ver"):
        with open("earley_table.txt", "w+", encoding="utf-8") as file:
            self.__printTableToFileHelper(file, tableType)

    def __printTableToFileHelper(self, file, tableType="ver"):
        maxRow = 0
        colNum = 0
        if tableType == "hor":
            for col in self.table:
                file.write("| %135s " % str(colNum).center(135))
                colNum += 1
                if len(col.states) > maxRow:
                    maxRow = len(col.states)

            file.write("|\n")

            for i in range(0, maxRow):
                for col in self.table:
                    if i >= len(col.states):
                        break
                    else:
                        file.write("| %135s " % str(col.states[i]).center(135))

                file.write("|\n")
        else:
            i = 0
            for col in self.table:
                file.write(HORIZONTAL_SYMBOL * 10 + " E_{0} - token: {1} ".format(i,
                                                                                  col.token) + HORIZONTAL_SYMBOL * 10 + "\n")
                for state in col.states:
                    file.write(str(state).ljust(len(str(state))) + "\n")
                i += 1
                file.write("\n")

    def getErrors(self):
        return self.semanticError

class TreeBuilder:
    def __init__(self, table, rules):
        self.table = table
        self.rules = rules
        self.pi = []
        self.tree = None
        self.file = None

    def buildTree(self):
        for state in self.table[-1]:
            if state.name == GAMMA_RULE and state.completed():
                self.tree = self.buildTreeHelper(self.table[0].states[0], len(self.table) - 1)
                return
        else:
            raise ValueError("Invalid earley table")

    def get_tree(self):
        return self.tree

    def buildTreeHelper(self, state, j):
        terms = state.production
        k = len(terms) - 1
        c = j

        result = TreeNode(Rule(state.name, state.production), self.table[j].token)

        while k > -1:
            if isinstance(terms[k], Rule):
                nextStates = self.searchStates(state, k, c, state.startColumn)
                k -= 1
                if len(nextStates) > 0:
                    result.addChild(self.buildTreeHelper(nextStates[-1], c))
                    c = nextStates[-1].startColumn.index
            else:
                k -= 1
                c -= 1

        return result

    def searchStates(self, inState, prodNum, columnNumber, i):
        subResult = []
        for state in self.table[columnNumber].states:
            if state.name == inState.production[prodNum].name and state.completed() and state != inState:
                subResult.append(state)

        result = []
        for state in subResult:
            if self.searchStatesHelper(state.name, state.startColumn, i):
                result.append(state)

        return result

    def searchStatesHelper(self, x, column, i):
        for state in column.states:
            if not state.completed() and \
                    isinstance(state.production[state.dotIndex], Rule) and \
                    state.production[state.dotIndex].name == x and \
                    state.startColumn == i:
                return True

        return False

    def printTreeToFile(self):
        if self.tree is not None:
            with open("Tree.txt", "w+", encoding="utf-8") as file:
                self.file = file
                self.__printTreeToFileHelper(self.tree)

    def printTreeToFileTest(self, trees):
        if trees is not None:
            with open("Tree1.txt", "w+", encoding="utf-8") as file:
                self.file = file
                for tree in trees:
                    self.__printTreeToFileHelper(tree)
                    self.file.write('\n')

    def __printTreeToFileHelper(self, current_node, indent='', nodeType='init'):
        lexemePart = '' if current_node.lexeme is None else ' Lexeme: ' + current_node.lexeme.lexeme
        name = repr(current_node.rule) + lexemePart

        if nodeType == 'last':
            start_shape = LEFT_SYMBOL + HORIZONTAL_SYMBOL * LEVEL_INDENT
        elif nodeType == 'mid':
            start_shape = VERTICAL_FORK + HORIZONTAL_SYMBOL * LEVEL_INDENT
        else:
            start_shape = ' '

        line = '{0}{1}{2}'.format(indent, start_shape, name)
        self.file.write(line + '\n')
        nextIndent = '{0}{1}'.format(indent,
                                     VERTICAL_SYMBOL + ' ' * (len(start_shape)) if nodeType == 'mid' else ' ' * (
                                             len(start_shape) + 1))

        if len(current_node.children) != 0:
            if len(current_node.children) == 1:
                self.__printTreeToFileHelper(current_node.children[0], nextIndent, 'last')
            else:
                for i in range(0, len(current_node.children) - 1):
                    self.__printTreeToFileHelper(current_node.children[i], nextIndent, 'mid')

                self.__printTreeToFileHelper(current_node.children[-1], nextIndent, 'last')

    def printTree(self):
        if self.tree is not None:
            self.__printTreeHelper(self.tree)

    def __printTreeHelper(self, node, indent='', nodeType='init'):
        if nodeType == 'last':
            start_shape = LEFT_SYMBOL + HORIZONTAL_SYMBOL * LEVEL_INDENT
        elif nodeType == 'mid':
            start_shape = VERTICAL_FORK + HORIZONTAL_SYMBOL * LEVEL_INDENT
        else:
            start_shape = ' '

        print('{0}{1}{2}'.format(indent, start_shape, node.state))
        nextIndent = '{0}{1}'.format(indent,
                                     VERTICAL_SYMBOL + ' ' * (len(start_shape)) if nodeType == 'mid' else ' ' * (
                                             len(start_shape) + 1))

        if len(node.children) != 0:
            if len(node.children) == 1:
                self.__printTreeHelper(node.children[0], nextIndent, 'last')
            else:
                for i in range(0, len(node.children) - 1):
                    self.__printTreeHelper(node.children[i], nextIndent, 'mid')

                self.__printTreeHelper(node.children[len(node.children) - 1], nextIndent, 'last')
