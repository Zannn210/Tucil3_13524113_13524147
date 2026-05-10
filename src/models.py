from dataclasses import dataclass
from typing import List

@dataclass
class Board:
    r: int #ukuran baris
    c: int #ukuran kolom
    grid: List[str]
    cost: List[List[int]]
    start_row: int = 0
    start_col: int = 0
    goal_row: int =0
    goal_col: int =0
    total_checkpoints: int = 0


@dataclass(frozen=True)
class State:
    row : int
    col: int
    next_checkpoint: int
    
@dataclass
class SlideResult:
    row: int #posisi baris setelah berhenti
    col: int #posisi kolom setelah berhenti
    move_cost : int #total cost dalam gerakan
    new_checkpoint: int
    valid : bool
    
@dataclass
class SearchResult:
    found : bool
    path : str 
    cost: int
    iterations : int
    trace: List[State]  
    time_ms : float