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
        file.seek(0)
        result = []
        lineNumber = 0
        for line in file.readlines():
            lineNumber += 1
            if bool(re.search('^<.+>->.+$', line)):
                marchingResult = re.search('^(<.+>)->', line)
                result.append(marchingResult.group(1))
            else:
                self.errors.append(GrammarParserError(lineNumber, GrammarParserErrorType.INVALID_RULE_STRUCT))
        for rule in result:
            self.rules.append(Rule(rule))

    def parseTxtRulesProductions(self, file):
        file.seek(0)
        lineNumber = 0
        for line in file.readlines():
            lineNumber += 1
            if bool(re.search('^<.+>->.+$', line)):
                marchingResult = re.search('^(<.+>)->', line)
                ruleName = marchingResult.group(1)
                rightSide = line.replace('\n', '').split('->')[1].split('|')

                rule = self.searchRule(ruleName)
                if rule:
                    for production in rightSide:
                        prodRule = self.searchRule(production)
                        if prodRule:
                            rule.add(prodRule)
                        else:
                            rule.add(production)
                else:
                    self.errors.append(GrammarParserError(lineNumber, GrammarParserErrorType.INVALID_RULE_NAME))

            else:
                self.errors.append(GrammarParserError(lineNumber, GrammarParserErrorType.INVALID_RULE_STRUCT))

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
        with open(filePath, 'r', encoding="utf-8") as jsonFile:
            sourceJson = json.load(jsonFile)

            for i, rule in enumerate(sourceJson):
                ruleName = rule['ruleName']
                if self.searchRule(ruleName) is None:
                    self.rules.append(Rule(ruleName))
                else:
                    self.errors.append(GrammarParserError(i, GrammarParserErrorType.REPEATED_RULE_NAME))

            if self.errors:
                ValueError("Invalid grammar")

            for i, rule in enumerate(sourceJson):
                workingRule = self.searchRule(rule['ruleName'])
                productions = rule["productions"]
                for production in productions:
                    prodAccum = Production()
                    for elem in production:
                        existRule = self.searchRule(elem)
                        if existRule:
                            prodAccum.add(existRule)
                        else:
                            match = re.search('reg{(.+)}', elem)
                            if match:
                                prodAccum.add(RegexpRule(match.group(1)))
                            else:
                                prodAccum.add(elem)
                    workingRule.add(prodAccum)
