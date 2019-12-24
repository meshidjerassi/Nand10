WRITE_KEYWORD = "<keyword>{}</keyword>\n"
WRITE_SYMBOL = "<symbol>{}</symbol>\n"
WRITE_IDENTIFIER = "<identifier>{}</identifier>\n"
CLASS_OPEN = "<class>\n" + WRITE_KEYWORD.format("class") + WRITE_IDENTIFIER + WRITE_SYMBOL.format("{")
CLASS_END = WRITE_SYMBOL.format("}") + "</class>\n"
CLASS_VAR_DEC_OPEN = "<classVarDec>\n" + WRITE_KEYWORD


class CompilationEngine:
    def __init__(self, tokenizer, output):
        self.tokenizer = tokenizer
        self.output = output

    def CompileClass(self):
        self.tokenizer.advance()  # class
        self.tokenizer.advance()  # class name
        self.output.write(CLASS_OPEN.format(self.tokenizer.identifier()))
        gc.VAR_TYPES.append(self.tokenizer.identifier())  # TODO: do I ever use this?
        self.tokenizer.advance()  # {
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == gc.KEYWORD:
                if self.tokenizer.keyWord in ["static", "field"]:
                    self.CompileClassVarDec()
                elif self.tokenizer.keyWord in ["constructor", "function", "method"]:
                    self.ComplieSubroutineDec()
        self.output.write(CLASS_END)

    def CompileClassVarDec(self):
        self.output.write(CLASS_VAR_DEC_OPEN.format(self.tokenizer.keyWord()))
        self.tokenizer.advance()  # type
        if self.tokenizer.tokenType() == gc.KEYWORD:
            self.output.write(WRITE_KEYWORD.format(self.tokenizer.keyWord()))
        else:
            self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
        self.tokenizer.advance()  # varName
        self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
        self.tokenizer.advance()  # , or ;
        while self.tokenizer.tokenType == gc.SYMBOL and self.tokenizer.symbol == ',':
            self.output.write(WRITE_SYMBOL.format(","))
            self.tokenizer.advance()  # varName
            self.output.write(WRITE_IDENTIFIER.format(self.tokenizer.identifier()))
            self.tokenizer.advance()  # symbol
        self.output.write(WRITE_SYMBOL.format(";"))
