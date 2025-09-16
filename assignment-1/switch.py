from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from typing import Literal

class Yard:
    # dict[track, set[track]] is an easy way to represent graphs
    def __init__(self, connectivity_list: list[tuple[int, int]]):
        # data will be a dict[track, set[track]]
        self._right_switches = defaultdict(set) # 1 -> 2 means you can move right 1 -> 2
        self._left_switches = defaultdict(set) # 2 -> 1 means you can move left 2 -> 1
        for track_1, track_2 in connectivity_list:
            self._right_switches[track_1].add(track_2) # add arc track_1 -> track_2
            self._left_switches[track_2].add(track_1) # add arc track_2 <- track_1
    
    def __repr__(self):
        return str(self._right_switches) + "\n" + str(self._left_switches)

    def get_all_right_connections(self, track: int) -> set[int]:
        return self._right_switches[track]
    
    def get_all_left_connections(self, track: int) -> set[int]:
        return self._left_switches[track]

class State:
    def __init__(self, state: list[list[str]]):
        self._data = defaultdict(list)
        for i, cars in enumerate(state):
            track = i + 1 # index 0 references track 1
            self._data[track].extend(cars) # add cars on that track in order to internal data structure
    
    @staticmethod
    def from_state(state: State) -> State:
        new_state = State([])
        new_state._data = deepcopy(state._data)
        return new_state
    
    def __repr__(self):
        return str(self._data)

    def is_contains_engine(self, track: int) -> bool:
        return "*" in self._data[track]

    def is_track_empty(self, track: int) -> bool:
        return len(self._data[track]) == 0
    
    def perform_internal_action(self, action: Action):
        from_track = action.connection[0]
        to_track = action.connection[1]

        if action.type == "l":
            left_most_from_track_y = self._data[from_track].pop(0)
            self._data[to_track].append(left_most_from_track_y)
        else:
            right_most_from_track_x = self._data[from_track].pop()
            self._data[to_track].insert(0, right_most_from_track_x)
    
    def get_track_with_engine(self) -> int:
        for track in self._data:
            if "*" in self._data[track]:
                return track
        raise Exception("State doesn't contain an engine!")

class Action:
    def __init__(self, type: Literal["l", "r"], connection: tuple[int, int]):
        self.type = type
        self.connection = connection
    
    def __repr__(self):
        return f"Action({self.type}, {self.connection})"
    
    def check_action(self, state: State) -> bool:
        connection = self.connection

        # if there aren't any trains to move
        if state.is_track_empty(connection[0]):
            return False

        return True

def possible_actions(yard: Yard, state: State) -> Action:
    engine_track = state.get_track_with_engine()
    all_right_connections = yard.get_all_right_connections(engine_track)
    all_left_connections = yard.get_all_left_connections(engine_track)

    possible_actions = []
    for other_track in all_right_connections:
        possible_actions.append(Action("r", (engine_track, other_track)))
        possible_actions.append(Action("l", (other_track, engine_track)))
    for other_track in all_left_connections:
        possible_actions.append(Action("l", (engine_track, other_track)))
        possible_actions.append(Action("r", (other_track, engine_track)))

    # filter out impossible ones
    possible_actions = list(filter(lambda action: action.check_action(state), possible_actions))

    return possible_actions

def result(action: Action, state: State) -> State:
    new_state = State.from_state(state)
    new_state.perform_internal_action(action)
    return new_state

# I love list comprehension
def expand(state: State, yard: Yard) -> list[State]:
    return [result(action, state) for action in possible_actions(yard, state)]
