from typing import Tuple


class SymbolTable:
    MOD = 31

    def __init__(self):
        self.__table = [[] for _ in range(SymbolTable.MOD)]

    @staticmethod
    def hash(value) -> int:
        if type(value) == int:
            return (value + SymbolTable.MOD) % SymbolTable.MOD

        if type(value) == str:
            return sum([ord(c) for c in value]) % SymbolTable.MOD

        if type(value) == chr:
            return ord(value) % SymbolTable.MOD

    def add(self, value) -> Tuple[int, int]:
        hash_value = SymbolTable.hash(value)

        if value in self.__table[hash_value]:
            return hash_value, self.__table[hash_value].index(value)

        self.__table[hash_value].append(value)

        return hash_value, len(self.__table[hash_value]) - 1
