from symbol_table import SymbolTable


if __name__ == '__main__':
    constants_table = SymbolTable()
    identifiers_table = SymbolTable()

    constants = [1, 2, 3, "Abc_asd", "a++++-$", 'c', 'd', 'a']
    identifiers = ["x", "y", "w", "minimum", "maximum"]

    for constant in constants:
        print("constant {} at position {}".format(constant, constants_table.add(constant)))

    for identifier in identifiers:
        print("identifier {} at position {}".format(identifier, identifiers_table.add(identifier)))

