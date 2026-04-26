import sys
from Parser.parsing import Parser

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        data = Parser.model_validate(lines)
        print(data)