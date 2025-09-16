from __future__ import annotations

from collections import deque

from switch import Yard, State, Action, expand_with_actions

class Node:
    def __init__(self, state: State, parent_node: Node = None, action: Action = None, depth: int = 0):
        self.state = state
        self.parent_node = parent_node
        self.action = action
        self.depth = depth

def dfs(yard: Yard, initial_state: State, goal_state: State, depth_limit: int) -> Node:
    fringe = deque([Node(initial_state)])
    while len(fringe) != 0:
        node = fringe.pop()
        if node.state == goal_state:
            return node
        elif node.depth > depth_limit:
            continue
        next_actions = expand_with_actions(node.state, yard)
        for state, action in next_actions:
            fringe.append(Node(state, node, action, node.depth + 1))
    return None

# we use iterative deepening (see PDF writeup for further details)
def blind_tree_search(yard: Yard, initial_state: State, goal_state: State) -> list[Action]:
    depth_limit = 0
    while True:
        print(f"Checking with depth_limit = {depth_limit}")
        result = dfs(yard, initial_state, goal_state, depth_limit)
        if result:
            break
        depth_limit += 1

    # we found a result! backtrack actions through the tree now
    actions = []
    while result.parent_node:
        actions.insert(0, result.action) # put at front
        result = result.parent_node
    
    return actions
