WRITE_KEYWORD = "<keyword>{}</keyword>\n"
WRITE_SYMBOL = "<symbol>{}</symbol>\n"
WRITE_IDENTIFIER = "<identifier>{}</identifier>\n"
CLASS_OPEN = "<class>\n" + WRITE_KEYWORD.format("class") + WRITE_IDENTIFIER + WRITE_SYMBOL.format("{")
CLASS_END = WRITE_SYMBOL.format("}") + "</class>\n"
CLASS_VAR_DEC_OPEN = "<classVarDec>\n" + WRITE_KEYWORD
CLASS_VAR_DEC_END = "</classVarDec>\n"
SUBROUTINE_OPEN = "<subroutineDec>\n" + WRITE_KEYWORD
SUBROUTINE_DEC_END = "</subroutineDec>\n"
SUBROUTINE_BODY_OPEN = "<subroutineBody>\n"
SUBROUTINE_BODY_END = "</subroutineBody>\n"


class CompilationEngine:
    def __init__(self, tokenizer, output):
        self.tokenizer = tokenizer
        self.output = output

    def CompileClass(self):
        self.tokenizer.advance()  # class
        self.tokenizer.advance()  # class name
        self.output.write(CLASS_OPEN.format(self.tokenizer.identifier()))
        consts.VAR_TYPES.append(self.tokenizer.identifier())  # TODO: do I ever use this?
        self.tokenizer.advance()  # {
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == consts.KEYWORDS:
                if self.tokenizer.keyWord in ["static", "field"]:
                    self.CompileClassVarDec()
                elif self.tokenizer.keyWord in ["constructor", "function", "method"]:
                    self.ComplieSubroutine()
        self.output.write(CLASS_END)

    def CompileClassVarDec(self):
        self.output.write(CLASS_VAR_DEC_OPEN.format(self.tokenizer.keyWord()))
        self.tokenizer.advance()  # type
        self._writeType()
        self.tokenizer.advance()  # varName
        self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
        self.tokenizer.advance()  # , or ;
        while self.tokenizer.tokenType == consts.SYMBOL and self.tokenizer.symbol == ',':
            self.output.write(WRITE_SYMBOL.format(","))
            self.tokenizer.advance()  # varName
            self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
            self.tokenizer.advance()  # , or ;
        self.output.write(WRITE_SYMBOL.format(";"))
        self.output.write(CLASS_VAR_DEC_END)

    def ComplieSubroutine(self):
        self.output.write(SUBROUTINE_OPEN.format(self.tokenizer.keyWord()))
        self.tokenizer.advance()  # retType
        self._writeType()
        self.tokenizer.advance()  # subRoutine name
        self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
        self.tokenizer.advance()  # (
        self.output.write(WRITE_SYMBOL.format("("))
        self.CompileParameterList()
        self.tokenizer.advance()  # )
        self.output.write(WRITE_SYMBOL.format(")"))
        self.output.write(SUBROUTINE_BODY_OPEN)
        self.tokenizer.advance()  # {
        self.output.write(WRITE_SYMBOL.format("{"))
        self.tokenizer.advance()  # var / statement
        while self.tokenizer.tokenType == consts.KEYWORDS and self.tokenizer.keyWord == "var":
            self.CompileVarDec()
        self.CompileStatements()
        self.output.write(WRITE_SYMBOL.format("}"))
        self.output.write(SUBROUTINE_BODY_END)
        self.output.write(SUBROUTINE_DEC_END)

    def CompileVarDec(self):
        self.output.write(WRITE_KEYWORD.format("var"))
        self.tokenizer.advance()  # type
        self._writeType()
        self.tokenizer.advance()  # var name
        self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier))
        self.tokenizer.advance()  # , or var or statement
        while self.tokenizer.tokenType == consts.SYMBOL:
            self.output.write(WRITE_SYMBOL.format(","))
            self.tokenizer.advance()  # varName
            self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
            self.tokenizer.advance()  # , or var or statement

    def _writeType(self):
        if self.tokenizer.tokenType() == consts.KEYWORDS:
            self.output.write(WRITE_KEYWORD.format(self.tokenizer.keyWord()))
        else:
            self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))

    def CompileParameterList(self):
        self.tokenizer.advance()  # type / statement
        if self.tokenizer.tokenType() == consts.IDENTIFIER or (
                self.tokenizer.tokenType() == consts.KEYWORDS and self.tokenizer.keyWord in consts.VAR_TYPES):
            self._writeType()
            self.tokenizer.advance()  # , or statement
            while self.tokenizer.tokenType == consts.SYMBOL:
                self.output.write(WRITE_SYMBOL.format(","))
                self.tokenizer.advance()  # varName
                self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
                self.tokenizer.advance()  # , or statement

    def CompileStatements(self):
        pass
