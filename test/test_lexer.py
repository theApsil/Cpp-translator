import unittest
from Lexer.LexicalAnalyzer import LexicalAnalyzer


class LexerTests(unittest.TestCase):
    def setUp(self):
        self.lexicalAnalyzer = LexicalAnalyzer('./tests/test_data/lexer_unit_test_file.cpp')
        self.lexicalAnalyzer.startParsing()

    def test_lexeme_type_plus(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(0), 'PLUS')

    def test_lexeme_type_increment(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(1), 'INCREMENT')

    def test_lexeme_type_minus(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(2), 'MINUS')

    def test_lexeme_type_decrement(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(3), 'DECREMENT')

    def test_lexeme_type_multiplication(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(4), 'MULTIPLICATION')

    def test_lexeme_type_division(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(5), 'DIVISION')

    def test_lexeme_type_mod(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(6), 'MOD')

    def test_lexeme_type_assignment(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(7), 'ASSIGNMENT')

    def test_lexeme_type_equal(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(8), 'EQUAL')

    def test_lexeme_type_not_equal(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(9), 'NOT_EQUAL')

    def test_lexeme_type_less_than(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(10), 'LESS_THAN')

    def test_lexeme_type_more_than(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(11), 'MORE_THAN')

    def test_lexeme_type_less_or_equal(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(12), 'LESS_OR_EQUAL')

    def test_lexeme_type_more_or_equal(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(13), 'MORE_OR_EQUAL')

    def test_lexeme_type_not(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(14), 'NOT')

    def test_lexeme_type_and(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(15), 'AND')

    def test_lexeme_type_or(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(16), 'OR')

    def test_lexeme_type_void(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(17), 'VOID')

    def test_lexeme_type_int(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(18), 'INT')

    def test_lexeme_type_long(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(19), 'LONG')

    def test_lexeme_type_short(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(20), 'SHORT')

    def test_lexeme_type_unsigned(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(21), 'UNSIGNED')

    def test_lexeme_type_bool(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(22), 'BOOL')

    def test_lexeme_type_float(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(23), 'FLOAT')

    def test_lexeme_type_double(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(24), 'DOUBLE')

    def test_lexeme_type_Char(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(25), 'CHAR')

    def test_lexeme_type_for(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(26), 'FOR')

    def test_lexeme_type_while(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(27), 'WHILE')

    def test_lexeme_type_if(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(28), 'IF')

    def test_lexeme_type_else(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(29), 'ELSE')

    def test_lexeme_type_true(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(30), 'TRUE')

    def test_lexeme_type_false(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(31), 'FALSE')

    def test_lexeme_type_include(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(32), 'INCLUDE')

    def test_lexeme_type_std(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(33), 'STD')

    def test_lexeme_type_main(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(34), 'MAIN')

    def test_lexeme_type_return(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(35), 'RETURN')

    def test_lexeme_type_cout(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(36), 'COUT')

    def test_lexeme_type_cin(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(37), 'CIN')

    def test_lexeme_type_abs(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(38), 'ABS')

    def test_lexeme_type_sqr(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(39), 'SQR')

    def test_lexeme_type_sqrt(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(40), 'SQRT')

    def test_lexeme_type_pow(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(41), 'POW')

    def test_lexeme_type_floor(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(42), 'FLOOR')

    def test_lexeme_type_ceil(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(43), 'CEIL')

    def test_lexeme_type_round_open_bracket(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(44), 'ROUND_OPEN_BRACKET')

    def test_lexeme_type_round_close_bracket(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(45), 'ROUND_CLOSE_BRACKET')

    def test_lexeme_type_curly_open_bracket(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(46), 'CURLY_OPEN_BRACKET')

    def test_lexeme_type_curly_close_bracket(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(47), 'CURLY_CLOSE_BRACKET')

    def test_lexeme_type_square_open_bracket(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(48), 'SQUARE_OPEN_BRACKET')

    def test_lexeme_type_square_close_bracket(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(49), 'SQUARE_CLOSE_BRACKET')

    def test_lexeme_type_semi_colon(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(50), 'SEMICOLON')

    def test_lexeme_type_colon(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(51), 'COLON')

    if __name__ == 'main':
        unittest.main()