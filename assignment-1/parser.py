# can parse LISP definitions into python objects

import re

from switch import Yard, State

"""
(define YARD-5 '((1 2) (1 3) (1 4)))
(define INIT-STATE-5 '((*) (a) (c b) (d))) ;Note c and b out of order
(define GOAL-STATE-5 '((* a b c d) empty empty empty))
"""

YARD_CONNECTIONS_PATTERN = r"\((\d+) ?(\d)+\)"
STATE_CARS_PATTERN = r"(?:\(((?:[\w*] ?)+)\))|(?:empty)"

def parse_yard(yard_string: str) -> Yard | None:
    connectivity_list = list(map(lambda x: (int(x[0]), int(x[1])), re.findall(YARD_CONNECTIONS_PATTERN, yard_string)))
    return Yard(connectivity_list)

def parse_state(state_string: str) -> State:
    state = map(lambda x: [] if "" in x else x, map(lambda x: x.split(" "), re.findall(STATE_CARS_PATTERN, state_string)))
    return State(state)

def parse_file(file_name: str) -> tuple[Yard | None, State | None, State | None]:
    with open(file_name) as file:
        lines = [line.rstrip() for line in file]
    if len(lines) < 3:
        return None, None, None
    
    yard = parse_yard(lines[0])
    init_state = parse_state(lines[1])
    goal_state = parse_state(lines[2])
    return yard, init_state, goal_state
