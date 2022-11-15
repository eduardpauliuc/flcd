from collections import defaultdict
from typing import Optional


class FiniteAutomata:
    def __init__(self):
        self.__states = []
        self.__alphabet = []
        self.__transitions = defaultdict(list)
        self.__initial_state = None
        self.__final_states = []

    def read_from_file(self, path: str) -> None:
        with open(path, "r") as f:
            f = open(path, "r")
            self.__states = f.readline().split()
            if not len(self.__states):
                raise RuntimeError("Empty states")

            self.__alphabet = f.readline().split()
            if not len(self.__states):
                raise RuntimeError("Empty alphabet")

            self.__initial_state = f.readline().strip()

            if not len(self.__states):
                raise RuntimeError("Empty initial state")
            if self.__initial_state not in self.__states:
                raise RuntimeError("Initial state not in list of states")

            self.__final_states = f.readline().split()
            for state in self.__final_states:
                if state not in self.__states:
                    raise RuntimeError(f"Final state {state} not in list of states")

            for line in f.read().split('\n'):
                line = line.strip()
                if not len(line):
                    continue

                items = line.split()
                origin = items[0]

                if origin not in self.__states:
                    raise RuntimeError(f"Origin {origin} not in list of states")

                for i in range(1, len(items), 2):
                    symbol, destination = items[i], items[i + 1]
                    if symbol not in self.__alphabet:
                        raise RuntimeError(f"Symbol {symbol} not in alphabet")
                    if destination not in self.__states:
                        raise RuntimeError(f"Destination {destination} not in list of states")
                    self.__transitions[origin].append((symbol, destination))

    def print_states(self) -> None:
        print("States: ", self.__states)

    def print_alphabet(self) -> None:
        print("Alphabet: ", self.__alphabet)

    def print_transitions(self) -> None:
        print("Transitions:")
        for key, transitions in self.__transitions.items():
            for (symbol, destination) in transitions:
                print(f"d({key},{symbol}) = {destination}")

    def print_initial_state(self) -> None:
        print("Initial state: ", self.__initial_state)

    def print_final_states(self) -> None:
        print("Final states: ", self.__final_states)

    def accepts(self, expression) -> bool:
        state = self.__initial_state

        for element in expression:
            transitions = list(filter(lambda el: el[0] == element, self.__transitions[state]))
            if len(transitions) == 0:
                return False
            elif len(transitions) > 1:
                print("Not a DFA!")
                return False

            state = transitions[0][1]

        return state in self.__final_states

    def getMatch(self, expression: str) -> Optional[str]:
        state = self.__initial_state
        last_good_match = ""
        match = ""
        index = 0
        while True:
            # while state not in self.__final_states:
            element = expression[index]
            index += 1

            transitions = list(filter(lambda el: el[0] == element, self.__transitions[state]))
            if len(transitions) == 0:
                break
            elif len(transitions) > 1:
                print("Not a DFA!")
                return None

            match += element
            state = transitions[0][1]

            if state in self.__final_states:
                last_good_match = match

                # return match if state in self.__final_states else None
        return last_good_match if len(last_good_match) else None


def print_menu():
    txt = "0 - Stop\n" \
          "1 - Print states\n" \
          "2 - Print alphabet\n" \
          "3 - Print transitions\n" \
          "4 - Print initial states\n" \
          "5 - Print Final states\n" \
          "6 - Check sequence in automata"

    print(txt)


def run():
    fa = FiniteAutomata()
    fa.read_from_file("integer_const.in")
    # fa.read_from_file("FA.in")

    running = True
    while running:
        print_menu()
        option = int(input("option: "))
        if option == 1:
            fa.print_states()
        elif option == 2:
            fa.print_alphabet()
        elif option == 3:
            fa.print_transitions()
        elif option == 4:
            fa.print_initial_state()
        elif option == 5:
            fa.print_final_states()
        elif option == 6:
            sequence = input("sequence to check: ")
            if fa.accepts(sequence):
                print("Accepted")
            else:
                print("Not accepted")
        elif option == 0:
            running = False
        else:
            print("Invalid option")


if __name__ == "__main__":
    run()
