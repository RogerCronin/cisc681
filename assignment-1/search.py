from collections import deque

from switch import Yard, State, Action, expand_with_actions

class Node:
    def __init__(self, state: State):
        self.__init__(state, None, None, 0)

    def __init__(self, state: State, parent_state: State, action: Action, depth: int):
        self.state = state
        self.parent_state = parent_state
        self.action = action
        self.depth = depth

def dfs(yard: Yard, initial_state: State, goal_state: State, depth_limit: int) -> Node:
    depth = 0
    fringe = deque(Node(initial_state))
    while len(fringe) != 0:
        node = fringe.pop()
        if node == goal_state:
            return node
        elif node.depth > depth_limit:
            continue
        for state, action in expand_with_actions(node.state, yard):
            fringe.append(Node(state, node, action, depth + 1))
    return None

# we use iterative deepening (see PDF writeup for further details)
def blind_tree_search(yard: Yard, initial_state: State, goal_state: State) -> list[Action]:
    depth_limit = 0
    while True:
        result = dfs(yard, initial_state, goal_state, depth_limit)
        if result:
            break
        depth_limit += 1
    print(result)
