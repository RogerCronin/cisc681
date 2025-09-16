# written for Python 3.13.7

import sys
from collections.abc import Callable

from switch import Yard, State, Action
from tests import base_tests, problem_1_tests, problem_2_tests, problem_3_tests
from search import blind_tree_search, heuristic_tree_search
from data import \
    yard_1, init_state_1, goal_state_1, \
    yard_2, init_state_2, goal_state_2, \
    yard_3, init_state_3, goal_state_3, \
    yard_4, init_state_4, goal_state_4, \
    yard_5, init_state_5, goal_state_5

def print_help():
    print("Usage:")
    print("  python main.py <test>")
    print("  python main.py blind <yard>")
    print("  python main.py heuristic <yard>")
    print("  python main.py graph <yard>")
    print()
    print("Tests: base, test1, test2, test3, full")
    print("Yards: YARD-1, YARD-2, YARD-3, YARD-4, YARD-5")
    print()
    print("Please check the writeup.pdf attached with this assignment's Canvas submission.")
    print("Run with Python 3.13.7!")

def execute_search(search: Callable[[Yard, State, State], list[Action]], yard_name: str):
    match yard_name:
        case "YARD-1" | "yard1" | "yard-1" | "yard_1":
            result = search(yard_1, init_state_1, goal_state_1)
        case "YARD-2" | "yard2" | "yard-2" | "yard_2":
            result = search(yard_2, init_state_2, goal_state_2)
        case "YARD-3" | "yard3" | "yard-3" | "yard_3":
            result = search(yard_3, init_state_3, goal_state_3)
        case "YARD-4" | "yard4" | "yard-4" | "yard_4":
            result = search(yard_4, init_state_4, goal_state_4)
        case "YARD-5" | "yard5" | "yard-5" | "yard_5":
            result = search(yard_5, init_state_5, goal_state_5)
        case _:
            print_help()
            return
    
    print(result)

def main():
    args = sys.argv[1:]
    n = len(args)

    if n == 1:
        if args[0] == "base":
            base_tests()
        elif args[0] == "test1":
            problem_1_tests()
        elif args[0] == "test2":
            problem_2_tests()
        elif args[0] == "test3":
            problem_3_tests()
        elif args[0] == "full":
            base_tests()
            problem_1_tests()
            problem_2_tests()
            problem_3_tests()
        else:
            print_help()
            return
        print("Tests passed!")
    elif n == 2:
        if args[0] == "blind":
            execute_search(blind_tree_search, args[1])
        elif args[0] == "heuristic":
            execute_search(heuristic_tree_search, args[1])
        elif args[0] == "graph":
            ...
    else:
        print_help()

if __name__ == "__main__":
    main()
