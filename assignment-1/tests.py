from collections import defaultdict

from switch import Yard, State, Action, possible_actions, result, expand
from data import \
    yard_1, init_state_1, other_state_1, \
    yard_2, init_state_2, \
    yard_3, init_state_3

def base_tests():
    test_yard_3 = Yard([(1, 2), (1, 3)])
    print("Asserting YARD-3 right connections have (1 -> 2, 1 -> 3)...")
    assert 2 in test_yard_3.get_all_right_connections(1)
    assert 3 in test_yard_3.get_all_right_connections(1)
    print("Asserting YARD-3 left connections have (1 <- 2, 1 <- 3)...")
    assert 1 in test_yard_3.get_all_left_connections(2)
    assert 1 in test_yard_3.get_all_left_connections(3)

    print("Asserting State.from_state returns an exact copy...")
    state_1 = State([["*"], ["a"]])
    state_2 = State.from_state(state_1)
    assert state_1 == state_2
    print("Asserting State.from_state returns a new object...")
    state_2._data = defaultdict(list)
    state_2._data[1] = []
    state_2._data[2].extend(["*", "a"])
    assert state_1 != state_2
    print("Asserting State.is_track_empty works as intended...")
    assert state_2.is_track_empty(1)
    assert not state_2.is_track_empty(2)
    print("Asserting State.perform_internal_action works to the right...")
    state_1_copy = State.from_state(state_1)
    state_2_copy = State.from_state(state_2)
    state_1_copy.perform_internal_action(Action("r", (1, 2)))
    assert state_1_copy == state_2_copy
    print("Asserting State.perform_internal_action works to the left...")
    state_1_copy.perform_internal_action(Action("l", (2, 1)))
    assert state_1_copy == state_1
    print("Asserting State.get_track_with_engine returns correct track...")
    assert state_1.get_track_with_engine() == 1
    assert state_2.get_track_with_engine() == 2

    # code already prevents actions without engines or actions with nonexistent switches
    print("Asserting Action.check_action checks for empty tracks...")
    assert Action("r", (1, 2)).check_action(state_1)
    assert not Action("r", (1, 2)).check_action(state_2)

def problem_1_tests():
    print("Asserting possible_actions check on INIT-STATE-1...")

    init_state_1_actions = possible_actions(yard_1, init_state_1)
    print(init_state_1_actions)

    """
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
    """

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
