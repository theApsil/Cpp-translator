from Parser.Presentation import *
from enum import Enum
import json


class GrammarParserErrorType(Enum):
    INVALID_RULE_NAME = 'GRAMMAR-PARSER-ERROR-INVALID_RULE_NAME'
    INVALID_RULE_STRUCT = 'GRAMMAR-PARSER-ERROR-INVALID_RULE_STRUCT'
    REPEATED_RULE_NAME = 'GRAMMAR-PARSER-ERROR-REPEATED_RULE_NAME'


class GrammarParserError:
    def __init__(self, lineNumber, errorType: GrammarParserErrorType):
        self.lineNumber = lineNumber
        self.type = errorType


class ParserGrammar:
    def __init__(self):
        self.rules = []
        self.errors = []

    def search_rule(self, ruleName):
        for rule in self.rules:
            if rule.name == ruleName:
                return rule
        
        return None

    def parseTxtRulesNames(self, file):
        # Finish this
        return None

    def parseTxtRulesProductions(self, file):
        # Finish this
        return None
    
    def parseTxtRules(self, filePath):
        file = open(filePath, 'r', encoding="utf-8")
        self.parseTxtRulesNames(file)
        self.parseTxtRulesProductions(file)

    def getRuleCount(self):
        return len(self.rules)
    
    def printRules(self):
        for rule in self.rules:
            print(repr(rule))

    def parseJsonRules(self, filePath):
        # Finish this
        return None
