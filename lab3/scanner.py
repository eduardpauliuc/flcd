import re
from curses.ascii import isspace
from enum import Enum
from typing import Optional

from fa.fa import FiniteAutomata
from lab2.symbol_table import SymbolTable
from lab3.lexical_exception import LexicalException


class PIFValueType(Enum):
    CONSTANT = 1
    IDENTIFIER = 2
    TOKEN = 3


class Scanner:
    constants_table: Optional[SymbolTable]
    identifiers_table: Optional[SymbolTable]

    def __init__(self, tokens_path, output_path):
        self.__output_path = output_path
        self.__tokens = []
        self.read_tokens(tokens_path)
        self.index = 0
        self.current_line = 1
        self.program = ""
        self.constants_table = None
        self.identifiers_table = None
        self.pif = []

        self.int_automata = FiniteAutomata()
        self.int_automata.read_from_file("../fa/integer_const.in")

        self.identifier_automata = FiniteAutomata()
        # self.identifier_automata.read_from_file("identifier.in")

    def read_tokens(self, tokens_path) -> None:
        with open(tokens_path, "r") as f:
            for x in f:
                self.__tokens.append(x.strip())

    def read_program(self, code_path):
        with open(code_path, "r") as f:
            f = open(code_path, "r")
            self.program = f.read()

    def skip_whitespaces(self):
        while self.index < len(self.program) and isspace(self.program[self.index]):
            if self.program[self.index] == '\n':
                self.current_line += 1
            self.index += 1

    def skip_comments(self):
        if self.index < len(self.program) and self.program[self.index: self.index + 2] == "//":
            while self.index < len(self.program) and self.program[self.index] != '\n':
                self.index += 1
            self.index += 1
            self.current_line += 1

    def check_int_constant(self) -> bool:
        match = self.int_automata.getMatch(self.program[self.index:])
        if match:
            position = self.constants_table.add(match)
            self.pif.append(("const", position))
            self.index += len(match)
            return True
        return False

    def check_constant(self) -> bool:
        # if self.check_int_constant():
        #     return True
        string_expression = re.compile(r"^\"([a-zA-Z0-9_+\-*/%<=>!:, ]*)\"")
        number_expression = re.compile(r"^(([+-]?[1-9]+[0-9]*)|0)")

        string_match = string_expression.match(self.program[self.index:])
        number_match = number_expression.match(self.program[self.index:])

        match = number_match if string_match is None else string_match
        # match = string_match

        if match is not None:
            value = self.program[self.index: self.index + match.end()]
            position = self.constants_table.add(value)
            self.pif.append(("const", position))
            self.index += match.end()
            return True
        else:
            return False

    def check_identifier(self) -> bool:
        identifier_expression = re.compile(r"^\$[_a-zA-Z]+[_a-zA-Z0-9]*")
        match = identifier_expression.match(self.program[self.index:])

        if match is not None:
            value = self.program[self.index: self.index + match.end()]
            position = self.identifiers_table.add(value)
            self.pif.append(("id", position))
            self.index += match.end()
            return True
        else:
            return False

    def check_token(self) -> bool:
        for token in self.__tokens:
            if self.program[self.index:].startswith(token):
                self.pif.append((token, -1))
                self.index += len(token)
                return True

        return False

    def read_next(self):
        current_index = self.index
        changed = True

        while changed:
            self.skip_whitespaces()
            self.skip_comments()
            changed = current_index != self.index
            current_index = self.index

        if self.index == len(self.program):
            return
        if self.current_line == 27:
            pass

        if self.check_constant() | self.check_token() | self.check_identifier():
            pass
        else:
            raise LexicalException("on line " + str(self.current_line) + " no matching keyword")

    def scan(self, code_path) -> Optional[str]:
        self.index = 0
        self.current_line = 1
        self.read_program(code_path)
        self.constants_table = SymbolTable()
        self.identifiers_table = SymbolTable()

        try:
            while self.index < len(self.program):
                self.read_next()

            self.create_output()
        except LexicalException as ex:
            print("Lexical exception:", ex)

        return None

    def create_output(self) -> None:
        with open("PIF.out", "w") as f:
            for item in self.pif:
                f.write(str(item) + '\n')

        with open("ST.out", "w") as f:
            f.write("--- CONSTANTS ---\n")
            f.write(str(self.constants_table) + '\n')
            f.write("\n--- IDENTIFIERS ---\n")
            f.write(str(self.identifiers_table) + '\n')


if __name__ == "__main__":
    scanner = Scanner("../lab1b/token.in", "output")
    scanner.scan("../lab1a/p1.ed")
    # scanner.scan("../lab1a/p2.ed")
    # scanner.scan("../lab1a/p3.ed")
    # scanner.scan("../lab1a/p1err.ed")
