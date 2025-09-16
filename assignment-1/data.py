from switch import Yard, State

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
