from collections import defaultdict

from switch import Yard, State, Action, possible_actions, result, expand, expand_with_actions
from examples.data import \
    yard_1, init_state_1, other_state_1, \
    yard_2, init_state_2, \
    yard_3, init_state_3, goal_state_1

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
    init_state_1_actions_expected = [Action("r", (1, 2)), Action("r", (1, 3)), Action("l", (2, 1))]
    init_state_1_actions = possible_actions(yard_1, init_state_1)
    assert set(init_state_1_actions_expected) == set(init_state_1_actions)
    print("Asserting possible_actions check on OTHER-STATE-1...")
    other_state_1_actions_expected = [Action("l", (5, 3)), Action("r", (4, 5)), Action("l", (5, 4)), Action("r", (5, 6)), Action("l", (6, 5))]
    other_state_1_actions = possible_actions(yard_1, other_state_1)
    assert set(other_state_1_actions_expected) == set(other_state_1_actions)

    print("Asserting possible_actions check on INIT-STATE-2...")
    init_state_2_actions_expected = [Action("r", (1, 2)), Action("l", (2, 1)), Action("r", (1, 5)), Action("l", (5, 1))]
    init_state_2_actions = possible_actions(yard_2, init_state_2)
    assert set(init_state_2_actions_expected) == set(init_state_2_actions)
    print("Asserting possible_actions check on NEXT-STATE-2...")
    next_state_2 = State([[], ["*", "d"], ["b"], ["a", "e"], ["c"]])
    next_state_2_actions_expected = [Action("l", (2, 1)), Action("r", (2, 3)), Action("l", (3, 2)), Action("r", (2, 4)), Action("l", (4, 2))]
    next_state_2_actions = possible_actions(yard_2, next_state_2)
    assert set(next_state_2_actions_expected) == set(next_state_2_actions)

    print("Asserting possible_actions check on INIT-STATE-3...")
    init_state_3_actions_expected = [Action("r", (1, 2)), Action("r", (1, 3)), Action("l", (2, 1)), Action("l", (3, 1))]
    init_state_3_actions = possible_actions(yard_3, init_state_3)
    assert set(init_state_3_actions_expected) == set(init_state_3_actions)
    print("Asserting possible_actions check on WEIRD-STATE-3...")
    weird_state_3 = State([["a", "b"], [], ["*"]])
    weird_state_3_actions_expected = [Action("r", (1, 3)), Action("l", (3, 1))]
    weird_state_3_actions = possible_actions(yard_3, weird_state_3)
    assert set(weird_state_3_actions_expected) == set(weird_state_3_actions)

def problem_2_tests():
    print("Asserting RIGHT 1 2 check on INIT-STATE-1...")
    right_1_2 = Action("r", (1, 2))
    right_1_2_state_expected = State([[], ["*", "e"], [], ["b", "c", "a"], [], ["d"]])
    right_1_2_state = result(right_1_2, init_state_1)
    assert right_1_2_state_expected == right_1_2_state
    print("Asserting LEFT 2 1 check on INIT-STATE-1...")
    left_2_1 = Action("l", (2, 1))
    left_2_1_state_expected = State([["*", "e"], [], [], ["b", "c", "a"], [], ["d"]])
    left_2_1_state = result(left_2_1, init_state_1)
    assert left_2_1_state_expected == left_2_1_state

    print("Asserting RIGHT 4 5 check on OTHER-STATE-1...")
    right_4_5_state_expected = State([[], ["e"], [], ["b", "c"], ["a", "*"], ["d"]])
    right_4_5_state = result(Action("r", (4, 5)), other_state_1)
    assert right_4_5_state_expected == right_4_5_state
    print("Asserting LEFT 5 4 check on OTHER-STATE-1...")
    left_5_4_state_expected = State([[], ["e"], [], ["b", "c", "a", "*"], [], ["d"]])
    left_5_4_state = result(Action("l", (5, 4)), other_state_1)
    assert left_5_4_state_expected == left_5_4_state
    print("Asserting RIGHT 5 6 check on OTHER-STATE-1...")
    right_5_6_state_expected = State([[], ["e"], [], ["b", "c", "a"], [], ["*", "d"]])
    right_5_6_state = result(Action("r", (5, 6)), other_state_1)
    assert right_5_6_state_expected == right_5_6_state
    print("Asserting LEFT 5 3 check on OTHER-STATE-1...")
    left_5_3_state_expected = State([[], ["e"], ["*"], ["b", "c", "a"], [], ["d"]])
    left_5_3_state = result(Action("l", (5, 3)), other_state_1)
    assert left_5_3_state_expected == left_5_3_state

def problem_3_tests():
    print("Asserting expand check on OTHER-STATE-1...")
    other_state_1_expansion_expected = [
        State([[], ["e"], ["*"], ["b", "c", "a"], [], ["d"]]), # LEFT 5 3
        State([[], ["e"], [], ["b", "c"], ["a", "*"], ["d"]]), # RIGHT 4 5
        State([[], ["e"], [], ["b", "c", "a", "*"], [], ["d"]]), # LEFT 5 4
        State([[], ["e"], [], ["b", "c", "a"], [], ["*", "d"]]), # RIGHT 5 6
        State([[], ["e"], [], ["b", "c", "a"], ["*", "d"], []]) # LEFT 6 5
    ]
    other_state_1_expansion = expand(other_state_1, yard_1)
    for state in other_state_1_expansion_expected: # can't use the set comparison thing since dicts are unhashable
        assert state in other_state_1_expansion
    
    print("Asserting expand_with_actions on INIT-STATE-3...")
    init_state_3_expansion_expected = [
        (State([[], ["*", "a"], ["b"]]), Action("r", (1, 2))), # RIGHT 1 2
        (State([[], ["a"], ["*", "b"]]), Action("r", (1, 3))), # RIGHT 1 3
        (State([["*", "a"], [], ["b"]]), Action("l", (2, 1))), # LEFT 2 1
        (State([["*", "b"], ["a"], []]), Action("l", (3, 1))) # LEFT 3 1
    ]
    init_state_3_expansion = expand_with_actions(init_state_3, yard_3)
    for state in init_state_3_expansion_expected:
        assert state in init_state_3_expansion

def debug_tests():
    State.number_of_cars_on_correct_track(init_state_1, goal_state_1)
