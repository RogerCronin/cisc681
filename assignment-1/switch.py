from __future__ import annotations # this has to be the first line, otherwise you can't do recursive type hinting

from collections import defaultdict
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
    
    def __repr__(self) -> str:
        return str(self._right_switches) + "\n" + str(self._left_switches)

    # returns all moves you can make going right track -> other_track
    def get_all_right_connections(self, track: int) -> set[int]:
        return self._right_switches[track]
    
    # returns all moves you can make going left other_track <- track
    def get_all_left_connections(self, track: int) -> set[int]:
        return self._left_switches[track]

class State:
    def __init__(self, state: list[list[str]]):
        self._data = defaultdict(list)
        for i, cars in enumerate(state):
            track = i + 1 # track indexing starts at 1, not 0
            self._data[track].extend(cars) # add ordered cars on that track to internal data structure
    
    # returns a new state that's a deep copy of the passed state
    # Python constructor overloading isn't that good so this has to be a static method
    @staticmethod
    def from_state(state: State) -> State:
        new_state = State([])
        new_state._data = defaultdict(list)
        for key, value in state._data.items(): # can't just shallow copy it, gotta do it the long way
            new_state._data[key] = [x for x in value]
        return new_state
    
    def __repr__(self) -> str:
        return str(self._data)

    def __eq__(self, other) -> bool:
        return self._data == other._data
    
    def __hash__(self) -> int:
        return hash(self._data)

    # returns whether there aren't cars on a particular track
    def is_track_empty(self, track: int) -> bool:
        return len(self._data[track]) == 0
    
    # returns the total number of cars on any track
    def count_number_of_cars(self) -> int:
        cars = 0
        for track in self._data:
            cars += len(self._data[track])
        return cars
    
    # returns the number of cars on a particular track
    def number_of_cars_on_track(self, track: int) -> int:
        return len(self._data[track])

    # performs the provided Action, modifying the internal data structure
    # as opposed to, like, returning a new State or something
    # note this doesn't do any error checking; that's done elsewhere in the program
    def perform_internal_action(self, action: Action):
        from_track = action.connection[0]
        to_track = action.connection[1]

        if action.type == "l":
            left_most_from_track_y = self._data[from_track].pop(0)
            self._data[to_track].append(left_most_from_track_y)
        else:
            right_most_from_track_x = self._data[from_track].pop()
            self._data[to_track].insert(0, right_most_from_track_x)
    
    # returns the track that contains the engine
    def get_track_with_engine(self) -> int:
        for track in self._data:
            if "*" in self._data[track]:
                return track
        raise Exception("State doesn't contain an engine!")

class Action:
    def __init__(self, type: Literal["l", "r"], connection: tuple[int, int]):
        self.type = type
        self.connection = connection

    def __repr__(self) -> str:
        return f"Action({self.type}, {self.connection})"
    
    def __eq__(self, other) -> bool:
        return self.type == other.type and self.connection == other.connection

    def __hash__(self) -> int:
        return hash((self.type, self.connection))

    # ensures the Action is possible to do given a state
    # this used to be a more important function but I did a bunch of refactoring and it's done elsewhere now
    def check_action(self, state: State) -> bool:
        connection = self.connection

        if state.is_track_empty(connection[0]): # if there aren't any trains to move,
            return False # then it's an invalid Action

        return True # passed all the checks, must be a valid Action

def possible_actions(yard: Yard, state: State) -> list[Action]:
    # we can only perform actions with the engine
    engine_track = state.get_track_with_engine()
    all_right_connections = yard.get_all_right_connections(engine_track)
    all_left_connections = yard.get_all_left_connections(engine_track)

    possible_actions = []
    for other_track in all_right_connections: # add Actions from engine -> other or engine <- other
        possible_actions.append(Action("r", (engine_track, other_track)))
        possible_actions.append(Action("l", (other_track, engine_track)))
    for other_track in all_left_connections: # add Actions from other -> engine or other <- engine
        possible_actions.append(Action("l", (engine_track, other_track)))
        possible_actions.append(Action("r", (other_track, engine_track)))
    # this should be all possible actions, right?

    # filter out impossible ones
    possible_actions = list(filter(lambda action: action.check_action(state), possible_actions))

    return possible_actions # boom, we have our list of possible actions

def result(action: Action, state: State) -> State:
    new_state = State.from_state(state) # make a deepcopy of the input state
    new_state.perform_internal_action(action) # perform the action
    return new_state # output the modified state

# I love list comprehension!
# isn't this code so beautiful?
def expand(state: State, yard: Yard) -> list[State]:
    return [result(action, state) for action in possible_actions(yard, state)]

# does the same but the list contains tuples of State and the Action it performed from previous state -> this one
def expand_with_actions(state: State, yard: Yard) -> list[tuple[State, Action]]:
    return [(result(action, state), action) for action in possible_actions(yard, state)]
