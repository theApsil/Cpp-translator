from Parser.ParseGrammar import *
from CodeGenerator.Generator import *
from SemanticalAnalyzer.SemanticAnalyzer import *

lexicalAnalyzer = LexicalAnalyzer('test.cpp')
lexicalAnalyzerResult = lexicalAnalyzer.startParsing()

print()
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

        generator = Generator(treeBuilder.tree)
        generator.generate()
        print(generator.resultCode)

        variableStorage = VariableStorage()
        semanticAnalyser = VariableSemanticAnalyser(treeBuilder.tree)
        semanticAnalyser.parse(treeBuilder.tree, variableStorage)

    print()