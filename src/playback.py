import os
import sys
from .models import Board, SearchResult
from .visualizer import print_board, RESET, BOLD, RED, GREEN, CYAN

IS_WINDOWS = sys.platform =="win32"

def _read_key() -> str:
    if IS_WINDOWS:
        import msvcrt
        ch = msvcrt.getwch()
        if ch in ('\x00', '\xe0'):
            ch2 = msvcrt.getwch()
            if ch2 == 'M':
                return 'RIGHT'
            if ch2 == 'K':
                return 'LEFT'
            return ''
        if ch == '\x1b':
            return 'ESC'
        return ch
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'C':
                        return 'RIGHT'
                    if ch3 =='D':
                        return 'LEFT'
                return 'ESC'
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
            
def _clear() -> None:
    os.system("cls" if IS_WINDOWS else "clear")

def run_playback(board: Board, result: SearchResult, start_step: int =0) -> None:
    if not result.found:
        print(f"{RED}Tidak ada solusi untuk di-playback.{RESET}")
        return
    total = len(result.path)
    step= max(0,min(start_step, total))
    
    def show(s: int) -> None:
        _clear()
        print(f"{CYAN}[Playback] Step {s}/{total}  |  <- -> navigasi  |  ESC = jump  |  q = keluar{RESET}")
        direction = result.path[s-1] if s > 0 else ""
        print_board(board, result.trace[s].row, result.trace[s].col, s, direction)
    
    show(step)
    
    while True:
        key = _read_key()
        
        if key in ('q', 'Q'):
            break
        elif key == 'RIGHT':
            step = min(step + 1,total)
            show(step)
        elif key == 'LEFT':
            step = max(step -1, 0)
            show(step)
        elif key == 'ESC':
            print(f"\n>> Lompat ke step (0-{total}): ", end="", flush=True)
            try:
                target = int(input())
                step = max(0, min(target, total))
                
            except ValueError:
                pass
            show(step)
            
        print("\n[Playback selesai]")
        
def save_solution(board: Board, result: SearchResult, algo: str, h_type: int, out_path: str) -> None:
    try:
        with open(out_path, "w") as f:
            f.write("=== Ice Sliding Puzzle Solver ===\n")
            h_label = f" (H{h_type})" if algo != "UCS" else ""
            f.write(f"Algoritma  : {algo}{h_label}\n")
            
            if not result.found:
                f.write("Status    : Tidak ada solusi\n")
                f.write(f"Iterasi    : {result.iterations}\n")
                f.write(f"Waktu      : {result.time_ms:.2f} ms\n")
            else:
                f.write(f"Solusi    : {result.path}\n")
                f.write(f"Cost      : {result.cost}\n")
                f.write(f"Status    : {result.iterations}\n")
                f.write(f"Waktu     : {result.time_ms:.2f} ms\n")
                
                for step, state in enumerate(result.trace):
                    header ="Initial" if step == 0 else f"Step {step} : {result.path[step-1]}"
                    f.write(header+ "\n")
                    for i, row in enumerate(board.grid):
                        line = ""
                        for j, ch in enumerate(row):
                            if i == state.row and j == state.col:
                                line+= 'Z'
                            elif ch == 'Z':
                                line +='*'
                            else:
                                line +=ch
                                
                        f.write(line + "\n")
                    f.write("\n")
        print(f"{GREEN}>> Solusi disimpan ke: {out_path}{RESET}")
    except IOError as e:
        print(f"{RED}[Error] Tidak bisa menyimpan file: {e}{RESET}")