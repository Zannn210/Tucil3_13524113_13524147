from .models import Board, SearchResult

RESET = "\033[0m" #warna default
BOLD = "\033[1m" #teks tebal
RED = "\033[31m" #merah
GREEN = "\033[32m" #hijau
YELLOW = "\033[33m" #kuning
CYAN = "\033[36m" #biru muda
WHITE = "\033[37m" #putih
BG_BLUE = "\033[44m" #background biru

def print_board(board: Board, pin_row: int, pin_col: int, step: int, direction: str="") -> None:
    if step == 0:
        print(f"{BOLD}\nInitial{RESET}")
    else:
        print(f"{BOLD}\nStep {step} :{direction}{RESET}")
        
    for i, row in enumerate(board.grid):
        line = ""
        for j, ch in enumerate(row):
            if i == pin_row and j == pin_col:
                line += f"{BOLD}{BG_BLUE}{WHITE}Z{RESET}"
            elif ch == 'X':
                line += f"{WHITE}X{RESET}"
            elif ch == 'O':
                line += f"{BOLD}{GREEN}O{RESET}"
            elif ch == 'L':
                line += f"{BOLD}{RED}L{RESET}"
            elif ch == 'Z':
                line += "*"
            elif ch.isdigit():
                line+= f"{YELLOW}{ch}{RESET}"
            else:
                line += ch
        print(line)
        
        
def print_solution(board: Board, result: SearchResult) -> None:
    if not result.found:
        return
    for step, state in enumerate(result.trace):
        direction = result.path[step-1] if step >0 else ""
        print_board(board, state.row, state.col, step, direction)