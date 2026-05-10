import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

# Import absolut - sekarang aman karena semua file temanmu sudah absolut
from src.parser import parse_input
from src.solver import search

COLORS = {
    'Z': '#2196F3',
    'O': '#4CAF50',
    'X': '#455A64',
    'L': '#F44336',
    '0': '#FFC107',
    '1': '#FFC107',
    '2': '#FFC107',
    '3': '#FFC107',
    '4': '#FFC107',
    '5': '#FFC107',
    '6': '#FFC107',
    '7': '#FFC107',
    '8': '#FFC107',
    '9': '#FFC107',
    '.': '#ECEFF1',
    ' ': '#ECEFF1',
    '*': '#BBDEFB',
}
DEFAULT_COLOR = '#ECEFF1'

class IcePuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ice Sliding Puzzle Solver")
        self.root.resizable(False, False)

        self.board = None
        self.result = None
        self.current_step = 0
        self.playing = False
        self.playback_speed = 500

        self.setup_ui()

    def setup_ui(self):
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas = tk.Canvas(self.left_frame, width=500, height=500, bg='white')
        self.canvas.pack()

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        # Algoritma
        algo_frame = tk.LabelFrame(self.right_frame, text="Algoritma")
        algo_frame.pack(fill=tk.X, pady=5)
        self.algo_var = tk.StringVar(value='A*')
        for mode in ['UCS', 'GBFS', 'A*']:
            tk.Radiobutton(algo_frame, text=mode, variable=self.algo_var,
                           value=mode, command=self.on_algo_change).pack(anchor=tk.W)

        # Heuristic
        heur_frame = tk.LabelFrame(self.right_frame, text="Heuristic")
        heur_frame.pack(fill=tk.X, pady=5)
        self.heur_var = tk.IntVar(value=1)
        self.heur_radios = []
        for h_type, name in [(1, "H1 - Manhattan"), (2, "H2 - Chebyshev"), (3, "H3 - Euclidean")]:
            rb = tk.Radiobutton(heur_frame, text=name, variable=self.heur_var, value=h_type)
            rb.pack(anchor=tk.W)
            self.heur_radios.append(rb)

        # Load Map
        tk.Button(self.right_frame, text="Load Map", command=self.load_map).pack(fill=tk.X, pady=2)

        # Run
        self.run_btn = tk.Button(self.right_frame, text="Run", command=self.run_solver, state=tk.DISABLED)
        self.run_btn.pack(fill=tk.X, pady=2)

        # Info
        info_frame = tk.LabelFrame(self.right_frame, text="Informasi Solusi")
        info_frame.pack(fill=tk.X, pady=5)
        self.info_vars = {
            'cost': tk.StringVar(value='-'),
            'time': tk.StringVar(value='- ms'),
            'iterations': tk.StringVar(value='-'),
            'solution': tk.StringVar(value='-')
        }
        for text, key in [('Cost:', 'cost'), ('Waktu:', 'time'), ('Iterasi:', 'iterations'), ('Solusi:', 'solution')]:
            row = tk.Frame(info_frame)
            row.pack(fill=tk.X, padx=5, pady=1)
            tk.Label(row, text=text, width=10, anchor='w').pack(side=tk.LEFT)
            tk.Label(row, textvariable=self.info_vars[key], anchor='w').pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Export
        self.export_btn = tk.Button(self.right_frame, text="Export Solution",
                                    command=self.export_solution, state=tk.DISABLED)
        self.export_btn.pack(fill=tk.X, pady=5)

        # Playback
        pb_frame = tk.LabelFrame(self.right_frame, text="Playback Solusi")
        pb_frame.pack(fill=tk.X, pady=5)
        nav_frame = tk.Frame(pb_frame)
        nav_frame.pack(fill=tk.X, pady=2)
        tk.Button(nav_frame, text="⏮ Prev", command=self.prev_step).pack(side=tk.LEFT, padx=2)
        tk.Button(nav_frame, text="Next ⏭", command=self.next_step).pack(side=tk.LEFT, padx=2)
        tk.Button(nav_frame, text="Jump", command=self.jump_to_step).pack(side=tk.LEFT, padx=2)

        play_frame = tk.Frame(pb_frame)
        play_frame.pack(fill=tk.X, pady=2)
        self.play_btn = tk.Button(play_frame, text="▶ Play", command=self.play)
        self.play_btn.pack(side=tk.LEFT, padx=2)
        tk.Button(play_frame, text="⏸ Pause", command=self.pause).pack(side=tk.LEFT, padx=2)
        tk.Button(play_frame, text="⏹ Stop", command=self.stop).pack(side=tk.LEFT, padx=2)

        speed_frame = tk.Frame(pb_frame)
        speed_frame.pack(fill=tk.X, pady=2)
        tk.Label(speed_frame, text="Speed (ms):").pack(side=tk.LEFT)
        self.speed_scale = tk.Scale(speed_frame, from_=50, to=2000, orient=tk.HORIZONTAL,
                                    command=self.set_speed)
        self.speed_scale.set(self.playback_speed)
        self.speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.step_label = tk.Label(pb_frame, text="Step: 0/0")
        self.step_label.pack()

        # Keyboard
        self.root.bind('<Left>', lambda e: self.prev_step())
        self.root.bind('<Right>', lambda e: self.next_step())
        self.root.bind('<Escape>', lambda e: self.jump_to_step())
        self.on_algo_change()

    def on_algo_change(self):
        state = tk.NORMAL if self.algo_var.get() in ('GBFS', 'A*') else tk.DISABLED
        for rb in self.heur_radios:
            rb.config(state=state)

    def load_map(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not filepath:
            return
        try:
            self.board = parse_input(filepath)
            self.result = None
            self.current_step = 0
            self.playing = False
            self.play_btn.config(text="▶ Play")
            self.run_btn.config(state=tk.NORMAL)
            self.export_btn.config(state=tk.DISABLED)
            self.clear_info()
            self.draw_grid()
            messagebox.showinfo("Info", "Peta berhasil dimuat.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat peta:\n{str(e)}")

    def clear_info(self):
        self.info_vars['cost'].set('-')
        self.info_vars['time'].set('- ms')
        self.info_vars['iterations'].set('-')
        self.info_vars['solution'].set('-')
        self.step_label.config(text="Step: 0/0")

    def run_solver(self):
        if self.board is None:
            return
        algo = self.algo_var.get()
        h_type = self.heur_var.get() if algo in ('GBFS', 'A*') else 1
        self.result = search(self.board, algo, h_type)

        if not self.result.found:
            messagebox.showinfo("Hasil", "Tidak ditemukan solusi.")
            self.clear_info()
            self.draw_grid()
            self.export_btn.config(state=tk.DISABLED)
            return

        self.info_vars['cost'].set(str(self.result.cost))
        self.info_vars['time'].set(f"{self.result.time_ms:.2f} ms")
        self.info_vars['iterations'].set(str(self.result.iterations))
        self.info_vars['solution'].set(' → '.join(self.result.path))
        self.export_btn.config(state=tk.NORMAL)

        self.current_step = 0
        self.playing = False
        self.play_btn.config(text="▶ Play")
        total = len(self.result.trace) - 1
        self.step_label.config(text=f"Step: 0/{total}")
        self.draw_grid()
        self.update_display()

    def export_solution(self):
        if not self.result or not self.result.found:
            return
        algo = self.algo_var.get()
        h_type = self.heur_var.get() if algo in ('GBFS', 'A*') else 1
        h_label = f"_H{h_type}" if algo != "UCS" else ""
        default_name = f"solution_{algo}{h_label}.txt"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=default_name,
            title="Simpan solusi sebagai"
        )
        if not filepath:
            return
        try:
            with open(filepath, 'w') as f:
                f.write("=== Ice Sliding Puzzle Solver ===\n")
                h_label_full = f" (H{h_type})" if algo != "UCS" else ""
                f.write(f"Algoritma  : {algo}{h_label_full}\n")
                f.write(f"Solusi     : {self.result.path}\n")
                f.write(f"Cost       : {self.result.cost}\n")
                f.write(f"Iterasi    : {self.result.iterations}\n")
                f.write(f"Waktu      : {self.result.time_ms:.2f} ms\n\n")
                for step, state in enumerate(self.result.trace):
                    header = "Initial" if step == 0 else f"Step {step} : {self.result.path[step-1]}"
                    f.write(header + "\n")
                    for i, row in enumerate(self.board.grid):
                        line = ""
                        for j, ch in enumerate(row):
                            if i == state.row and j == state.col:
                                line += 'Z'
                            elif ch == 'Z':
                                line += '*'
                            else:
                                line += ch
                        f.write(line + "\n")
                    f.write("\n")
            messagebox.showinfo("Sukses", f"Solusi berhasil disimpan ke:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan file:\n{e}")

    def get_tile_size(self):
        if self.board is None:
            return 30
        max_dim = max(self.board.r, self.board.c)
        return min(50, 500 // max_dim)

    def draw_grid(self):
        self.canvas.delete("all")
        if self.board is None:
            return
        rows, cols = self.board.r, self.board.c
        tile = self.get_tile_size()
        self.tile_size = tile
        self.canvas.config(width=cols * tile, height=rows * tile)
        for r in range(rows):
            for c in range(cols):
                x1 = c * tile
                y1 = r * tile
                x2 = x1 + tile
                y2 = y1 + tile
                ch = self.board.grid[r][c]
                color = COLORS.get(ch, DEFAULT_COLOR)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#90A4AE')
                if ch not in ('.', ' '):
                    self.canvas.create_text(c * tile + tile//2, r * tile + tile//2,
                                            text=ch, font=('Arial', 10, 'bold'),
                                            fill='white' if ch in ('Z','O','X','L') else 'black')

    def update_display(self):
        if self.board is None or self.result is None or not self.result.found:
            self.draw_grid()
            return
        self.draw_grid()
        trace = self.result.trace
        if not trace:
            return
        idx = max(0, min(self.current_step, len(trace) - 1))
        state = trace[idx]
        tile = self.tile_size
        r, c = state.row, state.col
        x1 = c * tile + 4
        y1 = r * tile + 4
        x2 = (c + 1) * tile - 4
        y2 = (r + 1) * tile - 4
        self.canvas.create_oval(x1, y1, x2, y2, fill='#FF9800', outline='#E65100', width=2)
        self.canvas.create_text(c * tile + tile//2, r * tile + tile//2,
                                text='P', font=('Arial', 12, 'bold'), fill='white')
        total = len(trace) - 1
        self.step_label.config(text=f"Step: {idx}/{total}")

    def next_step(self):
        if not self.result or not self.result.found:
            return
        max_idx = len(self.result.trace) - 1
        if self.current_step < max_idx:
            self.current_step += 1
            self.update_display()
            self.check_playback_end()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_display()

    def jump_to_step(self):
        if not self.result or not self.result.found:
            return
        total = len(self.result.trace) - 1
        step = simpledialog.askinteger("Lompat ke Step", f"Masukkan step (0-{total}):",
                                       parent=self.root, minvalue=0, maxvalue=total)
        if step is not None:
            self.current_step = step
            self.update_display()
            self.check_playback_end()

    def play(self):
        if not self.result or not self.result.found:
            return
        if self.current_step >= len(self.result.trace) - 1:
            self.current_step = 0
        self.playing = True
        self.play_btn.config(text="⏸ Pause", command=self.pause)
        self.auto_play()

    def pause(self):
        self.playing = False
        self.play_btn.config(text="▶ Play", command=self.play)

    def stop(self):
        self.playing = False
        if self.result and self.result.found:
            self.current_step = 0
            self.update_display()
        self.play_btn.config(text="▶ Play", command=self.play)

    def auto_play(self):
        if not self.playing:
            return
        max_idx = len(self.result.trace) - 1
        if self.current_step < max_idx:
            self.current_step += 1
            self.update_display()
            self.check_playback_end()
            self.root.after(self.playback_speed, self.auto_play)
        else:
            self.playing = False
            self.play_btn.config(text="▶ Play", command=self.play)

    def check_playback_end(self):
        if self.result and self.result.found and self.current_step == len(self.result.trace) - 1:
            self.playing = False
            self.play_btn.config(text="▶ Play", command=self.play)

    def set_speed(self, val):
        self.playback_speed = int(val)


if __name__ == "__main__":
    root = tk.Tk()
    app = IcePuzzleGUI(root)
    root.mainloop()