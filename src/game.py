from .models import Board, SlideResult

DIRECTIONS: dict[str, tuple[int,int]]={
    'U' : (-1,0), # atas
    'D' : (1,0), #bawah
    'L' : (0,-1), #kiri
    'R' : (0,1), #kanan
}

def slide(board: Board,row: int, col:int, dr:int, dc:int, next_cp: int) -> SlideResult:
    r,c = row, col
    total_cost = 0
    current_cp = next_cp
    while True:
        nr = r+dr
        nc = c+ dc
        
        if not(0 <= nr < board.r and 0 <= nc < board.c):
            return SlideResult(0, 0,0,0, False)
        
        tile = board.grid[nr][nc]
        if tile == 'X':
            break
        
        if tile =='L':
            return SlideResult(0, 0, 0, 0,False)
        
        r,c = nr,nc
        total_cost += board.cost[r][c]
        
        if tile.isdigit():
            cp_num =int(tile)
            if cp_num == current_cp:
                current_cp +=1
            elif cp_num > current_cp:
                return SlideResult(0,0,0,0, False)
            
        if tile == 'O':
            break
        
    if r == row and c == col:
        return SlideResult(0,0,0,0, False)
    
    return SlideResult(r, c, total_cost, current_cp, True)