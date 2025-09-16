# written for Python 3.13.7

from tests import base_tests, problem_1_tests, problem_2_tests, problem_3_tests
import sys

def print_help():
    print("Usage:")
    print("  python main.py <test>")
    print("  python main.py blind <yard>")
    print("  python main.py heuristic <yard>")
    print("  python main.py graph <yard>")
    print()
    print("Tests: base, test1, test2, test3")
    print("Yards: YARD-1, YARD-2, YARD-3, YARD-4, YARD-5")
    print()
    print("Please check the writeup.pdf attached with this assignment's Canvas submission.")
    print("Run with Python 3.13.7!")

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
        else:
            print_help()
            return
        print("Tests passed!")
    elif n == 2:
        if args[0] == "blind":
            ...
        elif args[0] == "heuristic":
            ...
        elif args[0] == "graph":
            ...
    else:
        print_help()

if __name__ == "__main__":
    main()
