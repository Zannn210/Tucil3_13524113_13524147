import math
from .models import State

#H1
def h_manhattan(state: State, goal_row: int, goal_col:int) -> int:
    return abs(state.row - goal_row) + abs(state.col - goal_col)

#H2
def h_chebyshev(state: State, goal_row: int, goal_col: int) -> int:
    return max(abs(state.row - goal_row), abs(state.col - goal_col))

#H3
def h_euclidean(state: State, goal_row: int, goal_col:int) -> float:
    dr = state.row - goal_row
    dc = state.col - goal_col
    
    return math.sqrt(dr * dr + dc *dc)

def heuristic(state: State, goal_row: int, goal_col: int, h_type: int) -> float:
    if h_type == 1:
        return float(h_manhattan(state, goal_row, goal_col))
    if h_type == 2:
        return float(h_chebyshev(state, goal_row, goal_col))
    if h_type == 3:
        return (h_euclidean(state, goal_row, goal_col))
    
    #default ke H1 jika input tidak dikenal
    return float(h_manhattan(state, goal_row, goal_col))
    