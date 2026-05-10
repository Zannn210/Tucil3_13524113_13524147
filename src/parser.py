from typing import Tuple
from .models import Board


def validate_board(board: Board) -> Tuple[bool, str]:
    has_start = False
    has_goal = False
    
    for i, row in enumerate(board.grid):
        if len(row) != board.c:
            return False, (f"Baris grid ke-{i} panjangnya {len(row)}, yang benar {board.r}")
        for ch in row:
            if ch == 'Z' : has_start = True
            if ch == 'O' : has_goal = True
    
    if not has_start:
        return False, "Tidak ditemukan karakter 'Z' (posisi awal)"
    if not has_goal:
        return False, "Tidak ditemukan karakter 'O' (titik tujuan)"
    
    if len(board.cost) != board.r:
        return False, (f"Jumlah baris cost {len(board.cost)}, yang benar {board.c}")
    for i, row in enumerate(board.cost):
        if len(row) !=  board.c:
            return False, (f"Baris cost ke-{i} panjangnya {len(row)}, yang benar {board.r}")
        
    return True, ""


def parse_input(filename: str) -> Board:
    try:
        with open(filename, "r") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]
    except FileNotFoundError:
        raise ValueError(f"File tidak ditemukan: '{filename}'")
    
    idx = 0
    
    try:
        parts = lines[idx].split()
        if len(parts) < 2:
            raise ValueError("Baris pertama harus memuat tepat dua angka (N M)")
        n, m = int(parts[0]), int(parts[1])
        idx += 1
    except (ValueError, IndexError):
        raise ValueError("Baris pertama harus berisi dua integer: N M")
    
    if n <=0 or m <= 0:
        raise ValueError(f"Ukuran papan tidak valid: N{n}, M{m}")
    
    if idx + n> len(lines):
        raise ValueError(f"File kurang baris grid: butuh {n}, tersedia {len(lines - idx)}")
    
    
    grid = lines[idx :idx+ n]
    idx += n
    
    if idx + n >len(lines):
        raise ValueError(f"File kurang baris cost: butuh {n}, tersedia {len(lines -idx)}")
    cost: list[list[int]] =[]
    for i in range(n):
        try:
            row_cost = list(map(int, lines[idx+i].split()))
        except ValueError:
            raise ValueError(f"Baris cost ke-{i} mengandung nilai bukan integer")
        cost.append(row_cost)
    idx+= n
    start_row = start_col =0
    goal_row= goal_col = 0
    max_cp= -1
    
    for i, row in enumerate(grid):
        for j, ch in enumerate(row):
            if ch == 'Z': start_row, start_col = i,j
            if ch == 'O': goal_row, goal_col = i, j
            if ch.isdigit():
                max_cp = max(max_cp, int(ch))
                
    total_checkpoint = max_cp + 1 if max_cp >= 0 else 0
    board = Board(
        r=n, c=m, grid= grid, cost=cost, start_row=start_row, start_col=start_col, goal_row=goal_row, goal_col=goal_col,total_checkpoints= total_checkpoint
    )
    
    valid, msg= validate_board(board)
    if not valid:
        raise ValueError(f"Input tidak valid: {msg}")
    
    return board