import heapq
import time
from typing import Dict, List, Tuple

from .models import Board, State, SearchResult
from .game import slide, DIRECTIONS
from .heuristic import heuristic

def compute_f(algo: str, g:int, state: State, goal_row: int, goal_col: int, h_type:int) -> float:
    h = heuristic(state, goal_row, goal_col, h_type)
    if algo == "UCS":
        return float(g)
    if algo == "GBFS":
        return float(h)
    if algo == "A*":
        return float(g) + h
    
    return float(g) + h

def search(board: Board, algo: str, h_type:int =1)-> SearchResult:
    t_start = time.perf_counter()
    init_state = State(board.start_row, board.start_col, 0)
    counter=0
    f0 = compute_f(algo, 0, init_state, board.goal_row,board.goal_col, h_type)
    
    heap: List[Tuple] = [(f0, counter, 0, init_state, "", [init_state])]
    
    best_cost: Dict[State, int] = {init_state: 0}
    iterations =0
    
    #loop utama
    while heap:
        f, _, g, state, path, trace = heapq.heappop(heap)
        iterations += 1
        
        if best_cost.get(state, float("inf")) < g:
            continue
        
        
        if(state.row == board.goal_row and state.col == board.goal_col and state.next_checkpoint == board.total_checkpoints):
            t_end = time.perf_counter()
            return SearchResult(found=True, path= path, cost=g,iterations=iterations, trace=trace,time_ms=(t_end-t_start) * 1000,)
        
        #ekspansi 4 arah
        for dir_name, (dr,dc) in DIRECTIONS.items():
            sr=slide(board,state.row, state.col, dr,dc, state.next_checkpoint)
            
            if not sr.valid:
                continue
            
            next_state= State(sr.row, sr.col, sr.new_checkpoint)
            new_g = g + sr.move_cost
            
            if new_g >= best_cost.get(next_state, float("inf")):
                continue
            
            best_cost[next_state] = new_g
            counter+=1
            f_next = compute_f(algo, new_g,next_state,board.goal_row, board.goal_col, h_type)
            
            heapq.heappush(heap, (f_next, counter, new_g, next_state, path + dir_name, trace+[next_state],))
            
            
    t_end = time.perf_counter()
    return SearchResult(found=False, path="",cost=0, iterations=iterations, trace=[],time_ms=(t_end-t_start) * 1000,)