import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.parser import parse_input
from src.solver import search
from src.visualizer import print_solution, BOLD, RESET, RED, GREEN, YELLOW, CYAN
from src.playback import run_playback, save_solution



def prompt_algo() -> str:
    while True:
        algo = input(">> Algoritma apa yang anda pilih? (UCS/GBFS/A*): ").strip().upper()
        if algo in ("UCS", "GBFS", "A*"):
            return algo
        print(f"{RED}[Error] Pilihan tidak valid. Masukkan: UCS, GBFS, atau A*{RESET}")
        
def prompt_heuristic()-> int:
    mapping = {"H1":1, "H2":2, "H3": 3, "1":1, "2":2, "3":3}
    while True:
        h = input(">> Heuristik apa yang anda pilih? (H1/H2/H3)\n   H1=Manhattan | H2=Chebyshev | H3= Euclidean\n>>").strip().upper()
        if h in mapping:
            return mapping[h]
        print(f"{RED}[Error] Pilihan tidak valid. Masukkan: H1, H2, atau H3{RESET}")
        
def yes_or_no(prompt: str) -> bool:
    ans = input(prompt).strip().lower()
    return ans in ("ya", "y")

def main() -> None:
    filename = input("Masukkan file input (Contoh: test/test1.txt): ").strip()
    try:
        board = parse_input(filename)
    except ValueError as e:
        print(f"{RED}[Error] {e}{RESET}")
        sys.exit(1)
    info = f"{GREEN}[OK] Papan {board.r}x{board.c} berhasil dibaca"
    if board.total_checkpoints > 0:
        info += f" | Checkpoint: 0 s/d {board.total_checkpoints -1}"
    print(info + RESET)
    
    print()
    algo = prompt_algo()
    h_type = prompt_heuristic() if algo != "UCS" else 1
    
    h_label = f" (H{h_type})" if algo != "UCS" else ""
    print(f"\n{YELLOW}>> Mencari solusi dengan {algo}{h_label}...{RESET}")
    result = search(board, algo, h_type)
    
    print()
    if result.found:
        print(f"{BOLD}{GREEN}Solusi yang ditemukan : {result.path}{RESET} ")
        print(f"{BOLD}cost dari solusi    : {result.cost}{RESET}")
        print_solution(board, result)
    else:
        print(f"{RED}{BOLD}Tidak ada solusi yang ditemukan.{RESET}")
    
    print(f"\n{BOLD}>> Waktu eksekusi      : {result.time_ms:.2f} ms{RESET}")
    print(f"\n{BOLD}>> Banyak iterasi      : {result.iterations} iterasi{RESET}")
    
    
    if result.found:
        print()
        if yes_or_no(">> Apakah anda ingin melakukan playback? (Ya/Tidak): "):
            try:
                start = int(input(f">> Pada step berapa anda ingin melakukan playback (0-{len(result.path)}): ").strip())
            except ValueError:
                start = 0
            run_playback(board, result, start)
        
    print()
    if yes_or_no(">> Apakah anda ingin menyimpan solusi? (Ya/Tidak): "):
        out_path = input(">> Nama file output (contoh: solusi.txt): ").strip()
        save_solution(board, result, algo, h_type, out_path)
        if result.found:
            print(f">> Solusi disimpan pada {out_path}")
            
if __name__ == "__main__":
    main()