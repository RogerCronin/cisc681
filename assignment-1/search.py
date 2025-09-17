from __future__ import annotations

from heapq import heappush, heappop
from collections import deque
from typing import Callable

from switch import Yard, State, Action, expand_with_actions

# node contains the current State, the previous State / Node, the action that took it from the previous state to this one,
# and the depth this node is at in the search tree
class Node:
    def __init__(self, state: State, parent_node: Node | None = None, action: Action | None = None, depth: int = 0):
        self.state = state
        self.parent_node = parent_node
        self.action = action
        self.depth = depth

# takes a Node containing a goal state and returns the list of Actions it took from the initial state to that one
# we have to backtrack it through Node.parent_node
def backtrack_actions_through_tree(node: Node) -> list[Action]:
    actions = []
    while node.parent_node:
        actions.insert(0, node.action) # put at front
        node = node.parent_node
    return actions

def dfs(yard: Yard, initial_state: State, goal_state: State, depth_limit: int) -> Node | None:
    fringe = deque([Node(initial_state)]) # we use a deque instead of a list cause it's faster
    while len(fringe) != 0: # while we still have states to process,
        node = fringe.pop()
        if node.state == goal_state: # if the current state is a goal state, we're done!
            return node
        elif node.depth > depth_limit: # if the current state is too deep, ignore
            continue
        next_actions = expand_with_actions(node.state, yard) # otherwise get the next states we can go to
        for state, action in next_actions: # add them to the fringe, increasing the depth by 1
            fringe.append(Node(state, node, action, node.depth + 1))
    return None # if we exhausted the fringe, we couldn't find a solution...

# my heuristic is total number of cars - number of cars in the goal state
# this function generates a valid f(n) = g(n) + h(n) with... uh... monads?
def f_factory(number_of_cars: int, end_track: int) -> Callable[[Node], int]:
    return lambda node: node.depth + (number_of_cars - node.state.number_of_cars_on_track(end_track))

def dijkstras(yard: Yard, initial_state: State, goal_state: State) -> Node | None:
    # make our f(n) cost function
    number_of_cars = initial_state.count_number_of_cars()
    end_track = goal_state.get_track_with_engine()
    f = f_factory(number_of_cars, end_track)

    # custom node that uses our f(n) as a comparator, needed for Python heapq
    class ComparisonNode(Node):
        def __lt__(self, other):
            return f(self) < f(other)

    root_node = ComparisonNode(initial_state)
    fringe = []
    heappush(fringe, root_node) # make a heap and push our initial state node to it
    while len(fringe) != 0: # while we still have states to process,
        node = heappop(fringe)
        if node.state == goal_state: # if the current state is a goal state, we're done!
            return node
        next_actions = expand_with_actions(node.state, yard) # otherwise get the next states we can go to
        for state, action in next_actions:
            child_node = ComparisonNode(state, node, action, node.depth + 1)
            heappush(fringe, child_node) # add them to the fringe, increasing the depth by 1
    return None # if we exhausted the fringe, we couldn't find a solution...

def graph_search(yard: Yard, initial_state: State, goal_state: State) -> Node | None:
    # this is almost identical to dijkstras except we keep track of visited states with a set
    number_of_cars = initial_state.count_number_of_cars()
    end_track = goal_state.get_track_with_engine()
    f = f_factory(number_of_cars, end_track)

    class ComparisonNode(Node):
        def __lt__(self, other):
            return f(self) < f(other)
    
    closed = set() # keeps a list of states so we don't accidentally backtrack in the search graph
    root_node = ComparisonNode(initial_state)
    fringe = []
    heappush(fringe, root_node)
    while len(fringe) != 0:
        node = heappop(fringe)
        if node.state == goal_state:
            return node
        state_representation = str(node.state) # we have to use this intermediary representation cause python can't hash dicts
        if not state_representation in closed:
            closed.add(state_representation) # if we're checking out a new state, add it to the closed set
            next_actions = expand_with_actions(node.state, yard)
            for state, action in next_actions:
                child_node = ComparisonNode(state, node, action, node.depth + 1)
                heappush(fringe, child_node)
    return None

# we use iterative deepening (see PDF writeup for further details)
def blind_tree_search(yard: Yard, initial_state: State, goal_state: State) -> list[Action]:
    depth_limit = 0
    while True: # forever,
        print(f"Checking with depth limit {depth_limit + 1}...")
        result = dfs(yard, initial_state, goal_state, depth_limit) # do dfs at this depth
        if result: # if we found a result, yay!
            break
        depth_limit += 1 # otherwise increase the depth by one and retry
    
    print("Found a solution!")
    return backtrack_actions_through_tree(result)

# I think heuristic_tree_search and heuristic_graph_search are pretty self explanatory, no?

def heuristic_tree_search(yard: Yard, initial_state: State, goal_state: State) -> list[Action]:
    result = dijkstras(yard, initial_state, goal_state)
    if not result:
        raise Exception("A* tree search failed to find a path")
    
    print("Found a solution!")
    return backtrack_actions_through_tree(result)

def heuristic_graph_search(yard: Yard, initial_state: State, goal_state: State) -> list[Action]:
    result = graph_search(yard, initial_state, goal_state)
    if not result:
        raise Exception("A* graph search failed to find a path")

    print("Found a solution!")
    return backtrack_actions_through_tree(result)
