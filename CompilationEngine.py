import LexicalElements as consts

WRITE_KEYWORD = "<keyword>{}</keyword>\n"
WRITE_SYMBOL = "<symbol>{}</symbol>\n"
WRITE_IDENTIFIER = "<identifier>{}</identifier>\n"

CLASS_OPEN = "<class>\n" + WRITE_KEYWORD.format("class") + WRITE_IDENTIFIER + WRITE_SYMBOL.format("{")
CLASS_END = WRITE_SYMBOL.format("}") + "</class>\n"
CLASS_VAR_DEC_OPEN = "<classVarDec>\n" + WRITE_KEYWORD
CLASS_VAR_DEC_END = "</classVarDec>\n"
SUBROUTINE_DEC_OPEN = "<subroutineDec>\n" + WRITE_KEYWORD
SUBROUTINE_DEC_END = "</subroutineDec>\n"
SUBROUTINE_BODY_OPEN = "<subroutineBody>\n"
SUBROUTINE_BODY_END = "</subroutineBody>\n"
STATEMENTS_OPEN = "<statements>\n"
STATEMENTS_END = "</statements>\n"
A_STATEMENT_OPEN = "<{}Statements>\n"
A_STATEMENT_END = "</{}Statements>\n"
EXP_OPEN = "<expression>\n"
EXP_END = "</expression>\n"

# todo: term explist intconst stringconst


class CompilationEngine:
    def __init__(self, tokenizer, output):
        self.tokenizer = tokenizer
        self.output = output
        self.subRoutines = []

    def CompileClass(self):
        self.tokenizer.advance()  # class
        self.tokenizer.advance()  # class name
        self.output.write(CLASS_OPEN.format(self.tokenizer.identifier()))
        consts.VAR_TYPES.append(self.tokenizer.identifier())  # TODO: do I ever use this?
        self.tokenizer.advance()  # {
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == "keyWord":
                if self.tokenizer.keyWord in consts.CLASS_VARS:
                    self.CompileClassVarDec()
                elif self.tokenizer.keyWord in consts.SUB_ROUTINES:
                    self.ComplieSubroutine()
        self.output.write(CLASS_END)

    def CompileClassVarDec(self):
        self.output.write(CLASS_VAR_DEC_OPEN.format(self.tokenizer.keyWord()))
        self.tokenizer.advance()  # type
        self._writeType()
        self.tokenizer.advance()  # varName
        self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
        self.tokenizer.advance()  # , or ;
        while self.tokenizer.tokenType() == "symbol" and self.tokenizer.symbol == ',':
            self.output.write(WRITE_SYMBOL.format(","))
            self.tokenizer.advance()  # varName
            self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
            self.tokenizer.advance()  # , or ;
        self.output.write(WRITE_SYMBOL.format(";"))
        self.output.write(CLASS_VAR_DEC_END)

    def ComplieSubroutine(self):
        self.output.write(SUBROUTINE_DEC_OPEN.format(self.tokenizer.keyWord()))
        self.tokenizer.advance()  # retType
        self._writeType()
        self.tokenizer.advance()  # subRoutine name
        self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
        self.subRoutines.append(self.tokenizer.identifier())
        self.tokenizer.advance()  # (
        self.output.write(WRITE_SYMBOL.format("("))
        self.CompileParameterList()
        self.tokenizer.advance()  # )
        self.output.write(WRITE_SYMBOL.format(")"))
        self.output.write(SUBROUTINE_BODY_OPEN)
        self.tokenizer.advance()  # {
        self.output.write(WRITE_SYMBOL.format("{"))
        self.tokenizer.advance()  # var / statement
        while self.tokenizer.tokenType() == "keyWord" and self.tokenizer.keyWord == "var":
            self.CompileVarDec()
        self.CompileStatements()
        self.output.write(WRITE_SYMBOL.format("}"))
        self.output.write(SUBROUTINE_BODY_END)
        self.output.write(SUBROUTINE_DEC_END)

    def CompileVarDec(self):
        # todo: verdec open
        self.output.write(WRITE_KEYWORD.format("var"))
        self.tokenizer.advance()  # type
        self._writeType()
        self.tokenizer.advance()  # var name
        self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier))
        self.tokenizer.advance()  # , or var or statement
        while self.tokenizer.tokenType() == "symbol":
            self.output.write(WRITE_SYMBOL.format(","))
            self.tokenizer.advance()  # varName
            self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
            self.tokenizer.advance()  # , or var or statement

    def _writeType(self):
        if self.tokenizer.tokenType() == "keyWord":
            self.output.write(WRITE_KEYWORD.format(self.tokenizer.keyWord()))
        else:
            self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))

    def CompileParameterList(self):
        # todo: paramlist open
        self.tokenizer.advance()  # type / statement
        if self.tokenizer.tokenType() == "identifier" or (
                self.tokenizer.tokenType() == "keyWord" and self.tokenizer.keyWord in consts.VAR_TYPES):
            self._writeType()
            self.tokenizer.advance()  # , or statement
            while self.tokenizer.tokenType() == "symbol":
                self.output.write(WRITE_SYMBOL.format(","))
                self.tokenizer.advance()  # varName
                self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
                self.tokenizer.advance()  # , or statement

    def CompileStatements(self):
        self.output.write(STATEMENTS_OPEN)
        while self.tokenizer.tokenType() == "keyWord" and self.tokenizer.keyWord in consts.STATEMENTS:
            if self.tokenizer.keyWord() == "let":
                self.CompileLet()
            elif self.tokenizer.keyWord() == "do":
                self.CompileDo()
            elif self.tokenizer.keyWord() == "while":
                self.CompileWhile()
            elif self.tokenizer.keyWord() == "return":
                self.CompileReturn()
            elif self.tokenizer.keyWord() == "if":
                self.CompileIf()
        self.output.write(STATEMENTS_END)

    def CompileLet(self):
        self.output.write(A_STATEMENT_OPEN.format("let"))
        self.output.write(WRITE_KEYWORD.format("let"))
        self.tokenizer.advance()  # var name
        self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
        self.tokenizer.advance()  # [ or =
        if self.tokenizer.symbol() == '[':
            self.output.write(WRITE_SYMBOL.format("["))
            self.CompileExpression()
            self.output.write(WRITE_SYMBOL.format("]"))
            self.tokenizer.advance()  # =
        self.output.write(WRITE_SYMBOL.format("="))
        self.CompileExpression()
        self.output.write(WRITE_SYMBOL.format(";"))
        self.tokenizer.advance()
        self.output.write(A_STATEMENT_END.format("let"))

    def CompileIf(self):
        self.output.write(A_STATEMENT_OPEN.format("if"))
        self.output.write(WRITE_KEYWORD.format("if"))
        self.tokenizer.advance()  # (
        self.output.write(WRITE_SYMBOL.format("("))
        self.CompileExpression()
        self.output.write(WRITE_SYMBOL.format(")"))
        self.tokenizer.advance()  # {
        self.output.write(WRITE_SYMBOL.format("{"))
        self.CompileStatements()
        self.output.write(WRITE_SYMBOL.format("}"))
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == "keyWord" and self.tokenizer.keyWord() == "else":
            self.output.write(WRITE_KEYWORD.format("else"))
            self.tokenizer.advance()  # {
            self.output.write(WRITE_SYMBOL.format("{"))
            self.CompileStatements()
            self.output.write(WRITE_SYMBOL.format("}"))
            self.tokenizer.advance()
        self.output.write(A_STATEMENT_END.format("if"))

    def CompileWhile(self):
        self.output.write(A_STATEMENT_OPEN.format("while"))
        self.output.write(WRITE_KEYWORD.format("while"))
        self.tokenizer.advance()  # (
        self.output.write(WRITE_SYMBOL.format("("))
        self.CompileExpression()
        self.output.write(WRITE_SYMBOL.format(")"))
        self.tokenizer.advance()  # {
        self.output.write(WRITE_SYMBOL.format("{"))
        self.CompileStatements()
        self.output.write(WRITE_SYMBOL.format("}"))
        self.tokenizer.advance()
        self.output.write(A_STATEMENT_END.format("while"))

    def CompileDo(self):
        self.output.write(A_STATEMENT_OPEN.format("do"))
        self.output.write(WRITE_KEYWORD.format("do"))
        self.tokenizer.advance()  # subroutine name / class name/var name
        if self.tokenizer.identifier() not in self.subRoutines:
            self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
            self.tokenizer.advance()  # .
            self.output.write(WRITE_SYMBOL.format("."))
        self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
        self.tokenizer.advance()  # (
        self.output.write(WRITE_SYMBOL.format("("))
        self.CompileExpressionList()
        self.tokenizer.advance()  # ) todo: check if delete
        self.output.write(WRITE_SYMBOL.format(")"))
        self.tokenizer.advance()  # ;
        self.output.write(WRITE_SYMBOL.format(";"))
        self.output.write(A_STATEMENT_END.format("do"))

    def CompileReturn(self):
        self.output.write(A_STATEMENT_OPEN.format("return"))
        self.output.write(WRITE_KEYWORD.format("return"))
        self.tokenizer.advance()  # statement or ;
        if self.tokenizer.tokenType() != "symbol" or self.tokenizer.symbol() != ';':
            self.CompileExpression()
        self.output.write(WRITE_SYMBOL.format(";"))
        self.output.write(A_STATEMENT_END.format("return"))

    def CompileExpression(self):
        self.output.write(EXP_OPEN)
        self.CompileTerm()
        self.tokenizer.advance()  # op or not todo: check if delete
        while self.tokenizer.tokenType() == "symbol" and self.tokenizer.symbol() in consts.OP:
            # todo: escaping of certain chars
            self.output.write(WRITE_SYMBOL.format(self.tokenizer.symbol()))
            self.tokenizer.advance()  # term
            self.CompileTerm()
            self.tokenizer.advance()  # symbol todo: check if delete
        self.output.write(EXP_END)
