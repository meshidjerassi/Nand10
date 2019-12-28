import glob
import os
import JackTokenizer as jt
import CompilationEngine as ce
from sys import argv


def main(path):
    """
    Creates parser object and code writer object, transfers the relevant commands to the relevant methods.
    :param path: file path
    :return: void
    """
    directory = []
    if os.path.isdir(path):
        directory = glob.iglob(os.path.join(path, "*.jack"))
    else:
        directory.append(path)
    for file in directory:
        f = open(file, 'r')
        tokenizer = jt.JackTokenizer(f)
        output = open(file[:-4] + "xml", 'w')
        cEngine = ce.CompilationEngine(tokenizer, output)
        cEngine.CompileClass()
        output.close()
        f.close()


if __name__ == "__main__":
    main(argv[1])
