# can parse LISP definitions into python objects

import re

from switch import Yard, State

"""
(define YARD-5 '((1 2) (1 3) (1 4)))
(define INIT-STATE-5 '((*) (a) (c b) (d))) ;Note c and b out of order
(define GOAL-STATE-5 '((* a b c d) empty empty empty))
"""

YARD_PATTERN = r"\(define (.+) '\(((\(\d+ \d+\) ?)+)\)\)"

def parse_yard(yard_string: str) -> Yard | None:
    matches = re.findall(YARD_PATTERN, yard_string)
    print(matches)
    if len(matches) != 2:
        return None
    connections_string = matches[1]
    print(connections_string)

def parse_state(state_string: str) -> State:
    ...

def parse_file(file_name: str) -> tuple[Yard | None, State | None, State | None]:
    with open(file_name) as file:
        lines = [line.rstrip() for line in file]
    if len(lines) < 3:
        return None, None, None
    
    yard = parse_yard(lines[0])
    init_state = parse_state(lines[1])
    goal_state = parse_state(lines[2])
    return yard, init_state, goal_state
