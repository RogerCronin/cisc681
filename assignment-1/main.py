# written for Python 3.13.7

import tests

def main():
    """
    yard_test = Yard([(1, 2)])
    init_state_test = State([["a", "*", "b"], ["c", "d"]])
    print(init_state_test)
    left_state_test = left(yard_test, init_state_test, (1, 2))
    print(left_state_test)
    right_state_test = right(yard_test, init_state_test, (1, 2))
    print(right_state_test)
    """

    """
    print("Usage: python main.py {<file> | --test [1..7]}")
    print("Note: Run this program with Python 3.13.7!")
    """

    tests.problem_3_tests()

if __name__ == "__main__":
    main()
