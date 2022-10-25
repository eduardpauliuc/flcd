from typing import Tuple

MOD = 31


class SymbolTable:
    def __init__(self):
        self.__table = [[] for _ in range(MOD)]

    @staticmethod
    def hash(value) -> int:
        if type(value) == int:
            return (value + MOD) % MOD

        if type(value) == str:
            return sum([ord(c) for c in value]) % MOD

        if type(value) == chr:
            return ord(value) % MOD

    def add(self, value) -> Tuple[int, int]:
        hash_value = SymbolTable.hash(value)

        if value in self.__table[hash_value]:
            return hash_value, self.__table[hash_value].index(value)

        self.__table[hash_value].append(value)

        return hash_value, len(self.__table[hash_value]) - 1
