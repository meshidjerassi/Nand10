KEYWORDS = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void",
            "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]

SYMBOL = ["(", ")", "{", "}", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]


def is_string_const(s):
    if s[0] == "\"" and s[-1] == "\"":
        return True
    else:
        return False


def is_identifier(s):
    if s[0] != "\"" and s[-1] != "\"":
        if s[0].isdigit():
            return False
        else:
            return True


def is_symbol(s):
    if s in SYMBOL:
        return True
    else:
        return False


def is_keyword(s):
    if s in KEYWORDS:
        return True
    else:
        return False
