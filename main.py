from Lexer import LexicalAnalyzer
from Parser import *
from CodeGenerator import Generator
from SemanticalAnalyzer import *


def get_code():
    lexicalAnalyzer = LexicalAnalyzer("test.cpp")
    lexicalAnalyzerResult = lexicalAnalyzer.startParsing()

    if lexicalAnalyzerResult:

        grammarParser = ParserGrammar()
        grammarParser.parseJsonRules('grammar.json')

        earley = Earley(grammarParser.rules, "<программа>")

        earleyParseResult = earley.parse(lexicalAnalyzer.lexemeArray)
        earley.printTableToFile()
        earley.printError()
        earleyTable = earley.table

        if earleyParseResult:
            treeBuilder = TreeBuilder(earleyTable, grammarParser.rules)
            treeBuilder.buildTree()
            treeBuilder.printTreeToFile()

            variableStorage = VariableStorage()
            semanticAnalyser = VariableSemanticAnalyser(treeBuilder.tree)
            semanticAnalyser.parse(treeBuilder.tree, variableStorage)

            generator = Generator(treeBuilder.tree)
            generator.generate()
            return generator.resultCode
        else:
            return "error", (earley.getErrors(), )
    else:
        return "error", lexicalAnalyzer.getErrors()
