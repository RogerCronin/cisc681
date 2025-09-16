from switch import Yard, State, Action, possible_actions, result, expand

yard_1 = Yard([(1, 2), (1, 3), (3, 5), (4, 5), (2, 6), (5, 6)])
init_state_1 = State([["*"], ["e"], [], ["b", "c", "a"], [], ["d"]])
goal_state_1 = State([["*", "a", "b", "c", "d", "e"], [], [], [], [], []])
other_state_1 = State([[], ["e"], [], ["b", "c", "a"], ["*"], ["d"]])

yard_2 = Yard([(1, 2), (1, 5), (2, 3), (2, 4)])
init_state_2 = State([["*"], ["d"], ["b"], ["a", "e"], ["c"]])
goal_state_2 = State([["*", "a", "b", "c", "d", "e"], [], [], [], []])

yard_3 = Yard([(1, 2), (1, 3)])
init_state_3 = State([["*"], ["a"], ["b"]])
goal_state_3 = State([["*", "a", "b"], [], []])

yard_4 = Yard([(1, 2), (1, 3), (1, 4)])
init_state_4 = State([["*"], ["a"], ["b", "c"], ["d"]])
goal_state_4 = State([["*", "a", "b", "c", "d"], [], [], []])

yard_5 = Yard([(1, 2), (1, 3), (1, 4)])
init_state_5 = State([["*"], ["a"], ["c", "b"], ["d"]])
goal_state_5 = State([["*", "a", "b", "c", "d"], [], [], []])

def problem_1_tests():
    init_state_1_actions = possible_actions(yard_1, init_state_1)
    print(init_state_1_actions)
    other_state_1_actions = possible_actions(yard_1, other_state_1)
    print(other_state_1_actions)

    init_state_2_actions = possible_actions(yard_2, init_state_2)
    print(init_state_2_actions)
    next_state_2 = State([[], ["*", "d"], ["b"], ["a", "e"], ["c"]])
    next_state_2_actions = possible_actions(yard_2, next_state_2)
    print(next_state_2_actions)

    init_state_3_actions = possible_actions(yard_3, init_state_3)
    print(init_state_3_actions)
    weird_state_3 = State([["a", "b"], [], ["*"]])
    weird_state_3_actions = possible_actions(yard_3, weird_state_3)
    print(weird_state_3_actions)

def problem_2_tests():
    print(init_state_1)

    right_1_2 = Action("r", (1, 2))
    right_1_2_state = result(right_1_2, init_state_1)
    print(right_1_2_state)

    left_2_1 = Action("l", (2, 1))
    left_2_1_state = result(left_2_1, init_state_1)
    print(left_2_1_state)

    print(other_state_1)

    print(result(Action("r", (4, 5)), other_state_1))
    print(result(Action("l", (5, 4)), other_state_1))
    print(result(Action("r", (5, 6)), other_state_1))
    print(result(Action("l", (5, 3)), other_state_1))

def problem_3_tests():
    print(other_state_1)
    new_states = expand(other_state_1, yard_1)
    for state in new_states:
        print(state) # so they're all on new lines
