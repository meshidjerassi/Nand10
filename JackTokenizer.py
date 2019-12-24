import sys
import LexicalElements as le

TAB = "\t"
NEW_LINE = "\n"
ASTRIX = '*'
SLASH = '/'
BACK_SLASH = '\\'
KEYWORD = "keyword"
SYMBOL = "symbol"


class JackTokenizer:
    """
    Handle one or multiple VM files, parses then and splits them into lines to send to the codeWriter obj
    """

    def __init__(self, f):
        """
        constructor, creates an array of parsed lines from the given path
        :param f: opened file
        """
        self.isComment = False
        self.continuesComment = False
        self.tokenized = []
        line = f.readline()
        while line:
            self.lineHandler(line)
            line = f.readline()

    def lineHandler(self, line):
        line = line.strip(NEW_LINE)
        line = line.strip(TAB)

        # Handles multiple lines comments
        if len(line) == 0:
            return
        self.multiLineCommentHandler(line)
        if self.isComment or self.continuesComment:
            self.isComment = False
            return
        line = self.removeSubComment(line)
        temp = ""
        # for i in range(len(line)+1):
        #     if le.is_keyword(temp):
        #         self.tokenized.append((temp, KEYWORD))  # appending keyword with lexical element tuple
        #         temp = ""
        #     if le.is_symbol(temp):
        #         self.tokenized.append((temp, SYMBOL))  # appending symbol with lexical element tuple
        #         temp = ""
        #     if i == len(line):
        #         break
        #     if len(temp)>=1:
        #         if le.is_symbol(temp[-1]):
        #             return #todo
        #   temp += line[i]
        return

    def multiLineCommentHandler(self, line):
        if not self.continuesComment:
            if len(line) >= 2:
                if line[0] == SLASH and line[1] == ASTRIX:
                    if line[-1] == SLASH and line[-2] == ASTRIX:
                        self.isComment = True
                    else:
                        self.continuesComment = True
        else:
            if line[-1] == SLASH and line[-2] == ASTRIX:
                self.isComment = True
                self.continuesComment = False

    def removeSubComment(self, line):
        if len(line) >= 2:
            for i in range(len(line)-1):
                if line[i] == line[i+1] == SLASH:
                    return line[:i]
        return line




def main():
    with open(sys.argv[1]) as fp:
        j = JackTokenizer(fp)
        for i in range(len(j.tokenized)):
            print("Token named: "+j.tokenized[i][0] + " typed: " + j.tokenized[i][1])



if __name__ == "__main__":
    main()
#
#
#
#
#


