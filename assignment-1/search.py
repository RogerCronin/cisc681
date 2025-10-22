from __future__ import annotations

from heapq import heappush, heappop
from collections import deque
from typing import Callable
from time import perf_counter

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

def dfs(yard: Yard, initial_state: State, goal_state: State, depth_limit: int) -> tuple[Node | None, int]:
    nodes_expanded = 1
    fringe = deque([Node(initial_state)]) # we use a deque instead of a list cause it's faster
    while len(fringe) != 0: # while we still have states to process,
        node = fringe.pop()
        if node.state == goal_state: # if the current state is a goal state, we're done!
            return (node, nodes_expanded)
        elif node.depth > depth_limit: # if the current state is too deep, ignore
            continue
        next_actions = expand_with_actions(node.state, yard) # otherwise get the next states we can go to
        nodes_expanded += 1
        for state, action in next_actions: # add them to the fringe, increasing the depth by 1
            fringe.append(Node(state, node, action, node.depth + 1))
    return (None, nodes_expanded) # if we exhausted the fringe, we couldn't find a solution...

# my heuristic is total number of cars - number of cars on the correct goal state track
# this function generates a valid f(n) = g(n) + h(n) with... uh... monads?
# originally this was number of cars - number of cars on track 1 which is faster, but I think you might test on alternative end goals...
def f_factory(goal_state: State) -> Callable[[Node], int]:
    number_of_cars = goal_state.count_number_of_cars()
    return lambda node: node.depth + (number_of_cars - State.number_of_cars_on_correct_track(node.state, goal_state))

def dijkstras(yard: Yard, initial_state: State, goal_state: State) -> tuple[Node | None, int]:
    # make our f(n) cost function
    f = f_factory(goal_state)

    # custom node that uses our f(n) as a comparator, needed for Python heapq
    class ComparisonNode(Node):
        def __lt__(self, other):
            return f(self) < f(other)

    nodes_expanded = 1
    root_node = ComparisonNode(initial_state)
    fringe = []
    heappush(fringe, root_node) # make a heap and push our initial state node to it
    while len(fringe) != 0: # while we still have states to process,
        node = heappop(fringe)
        if node.state == goal_state: # if the current state is a goal state, we're done!
            return (node, nodes_expanded)
        next_actions = expand_with_actions(node.state, yard) # otherwise get the next states we can go to
        nodes_expanded += 1
        for state, action in next_actions:
            child_node = ComparisonNode(state, node, action, node.depth + 1)
            heappush(fringe, child_node) # add them to the fringe, increasing the depth by 1
    return (None, nodes_expanded) # if we exhausted the fringe, we couldn't find a solution...

def graph_search(yard: Yard, initial_state: State, goal_state: State) -> tuple[Node | None, int]:
    # this is almost identical to dijkstras except we keep track of visited states with a set
    f = f_factory(goal_state)

    class ComparisonNode(Node):
        def __lt__(self, other):
            return f(self) < f(other)
    
    closed = set() # keeps a list of states so we don't accidentally backtrack in the search graph
    nodes_expanded = 1
    root_node = ComparisonNode(initial_state)
    fringe = []
    heappush(fringe, root_node)
    while len(fringe) != 0:
        node = heappop(fringe)
        if node.state == goal_state:
            return (node, nodes_expanded)
        state_representation = str(node.state) # we have to use this intermediary representation cause python can't hash dicts
        if not state_representation in closed:
            closed.add(state_representation) # if we're checking out a new state, add it to the closed set
            next_actions = expand_with_actions(node.state, yard)
            nodes_expanded += 1
            for state, action in next_actions:
                child_node = ComparisonNode(state, node, action, node.depth + 1)
                heappush(fringe, child_node)
    return (None, nodes_expanded)

# we use iterative deepening (see PDF writeup for further details)
def blind_tree_search(yard: Yard, initial_state: State, goal_state: State, report_depth = True) -> list[Action]:
    depth_limit = 0

    start_time = perf_counter()
    while True: # forever,
        if report_depth:
            print(f"Checking with depth limit {depth_limit + 1}...")
        result, nodes_expanded = dfs(yard, initial_state, goal_state, depth_limit) # do dfs at this depth
        if result: # if we found a result, yay!
            break
        depth_limit += 1 # otherwise increase the depth by one and retry
    end_time = perf_counter()
    
    print(f"Found a solution with {nodes_expanded} expansions taking {round(end_time - start_time, 6)} seconds!")
    return backtrack_actions_through_tree(result)

# I think heuristic_tree_search and heuristic_graph_search are pretty self explanatory, no?

def heuristic_tree_search(yard: Yard, initial_state: State, goal_state: State) -> list[Action]:
    start_time = perf_counter()
    result, nodes_expanded = dijkstras(yard, initial_state, goal_state)
    end_time = perf_counter()

    if not result:
        raise Exception("A* tree search failed to find a path")
    
    print(f"Found a solution with {nodes_expanded} expansions taking {round(end_time - start_time, 6)} seconds!")
    return backtrack_actions_through_tree(result)

def heuristic_graph_search(yard: Yard, initial_state: State, goal_state: State) -> list[Action]:
    start_time = perf_counter()
    result, nodes_expaned = graph_search(yard, initial_state, goal_state)
    end_time = perf_counter()

    if not result:
        raise Exception("A* graph search failed to find a path")

    print(f"Found a solution with {nodes_expaned} expansions taking {round(end_time - start_time, 6)} seconds!")
    return backtrack_actions_through_tree(result)
