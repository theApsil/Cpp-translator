import re
from Lexer.Lexems import LexemeType
from Lexer.LexicalAnalyzer import LexicalAnalyzer


class TreeNode(object):
    def __init__(self, rule, lexeme):
        self.rule = rule
        self.lexeme = lexeme
        self.children = []

    def __repr__(self):
        return str(self.rule)

    def addChild(self, child):
        self.children = [child] + self.children