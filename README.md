# Tugas Kecil 3 IF2211 Strategi Algoritma
## Ice Sliding Puzzle Solver

--- 

## Deskripsi Program

Program ini menyelesaikan permainan **Ice Sliding Puzzle** menggunakan algoritma pathfinding. Dalam permainan ini, pin bergerak di atas permukaan es yang licin — sekali bergerak, pin tidak bisa berhenti sampai menabrak dinding. Program mencari jalur optimal dari posisi awal menuju titik tujuan menggunakan tiga algoritma: **UCS**, **GBFS**, dan **A\***.

---

## Fitur Program

- Membaca peta dari file `.txt`
- Validasi input secara otomatis
- Tiga algoritma pathfinding: UCS, GBFS, A*
- Tiga pilihan heuristik: Manhattan, Chebyshev, Euclidean
- Visualisasi papan step-by-step dengan warna terminal
- Playback interaktif menggunakan tombol keyboard
- Menyimpan solusi ke file `.txt`
- Menampilkan waktu eksekusi dan jumlah iterasi

---

## Struktur Repository

```
Tucil3_13524113_13524147/
├── src/
│   ├── models.py       <- Struktur data (Board, State, dll)
│   ├── parser.py       <- Pembaca dan validator file input
│   ├── game.py         <- Logika gerakan sliding
│   ├── heuristic.py    <- Fungsi heuristik H1/H2/H3
│   ├── solver.py       <- Algoritma UCS, GBFS, A*
│   ├── visualizer.py   <- Tampilan papan di terminal
│   └── playback.py     <- Playback interaktif + simpan file
├── test/
│   ├── test1.txt       <- Kasus uji
│   ├── test2.txt
│   └── ...
├── doc/
│   └── laporan.pdf
├── main.py               <- Entry point program
├── gui.py
└── README.md
```

---

## Requirement

- **Python 3.10** atau lebih baru
- Tidak memerlukan library eksternal (hanya menggunakan stdlib Python)

---

## Cara Menjalankan

### 1. Clone repository

```bash
git clone https://github.com/username/Tucil3_13524113_13524147.git
cd Tucil3_13524113_13524147
```

### 2. Jalankan program

```bash
python main.py
```

atau 

```bash
python3 main.py
```

jika menggunakan gui:
```bash
python gui.py
```

atau 

```bash
python3 gui.py
```

---

## Cara Menggunakan Program

Program akan meminta input secara interaktif:

```
Masukkan file input (Contoh: test/test1.txt): test/test1.txt
>> Algoritma apa yang anda pilih? (UCS/GBFS/A*): A*
>> Heuristik apa yang anda pilih? (H1/H2/H3): H1


>> Apakah anda ingin melakukan playback? (Ya/Tidak): Ya
>> Pada step berapa anda ingin melakukan playback (0-8): 0

>> Apakah anda ingin menyimpan solusi? (Ya/Tidak): Ya
>> Nama file output (contoh: solusi.txt): solusi.txt
>> Solusi disimpan pada solusi.txt
```

### Kontrol Playback

| Tombol | Fungsi |
|--------|--------|
| `->` (kanan) | Maju satu step |
| `<-` (kiri) | Mundur satu step |
| `ESC` | Lompat ke step tertentu |
| `q` | Keluar dari playback |

---

## Format File Input

```
N M
[N baris karakter papan]
[N baris cost per tile]
```

### Keterangan Simbol

| Simbol | Arti |
|--------|------|
| `*` | Tile kosong yang bisa dilewati |
| `X` | Dinding — pin berhenti tepat sebelumnya |
| `L` | Lava — game over jika pin melewatinya |
| `Z` | Posisi awal pin |
| `O` | Titik tujuan |
| `0`-`9` | Checkpoint yang wajib dilewati sesuai urutan |

### Contoh File Input

```
7 7
XXXXXXX
X0****X
X**X**X
X****OX
X1***LX
XZ**X*X
XXXXXXX
999 999 999 999 999 999 999
999 3 5 2 8 1 999
999 7 4 999 6 9 999
999 2 8 3 5 4 999
999 6 1 7 2 999 999
999 9 3 4 999 8 999
999 999 999 999 999 999 999
```
---

## Algoritma yang Diimplementasikan

### Uniform Cost Search (UCS)
Mengeksplorasi node berdasarkan cost aktual dari titik awal.
Menjamin solusi optimal namun bisa lambat karena mengeksplorasi banyak node.

```
f(n) = g(n)
```

### Greedy Best-First Search (GBFS)
Mengeksplorasi node berdasarkan estimasi jarak ke tujuan.
Lebih cepat namun tidak menjamin solusi optimal.

```
f(n) = h(n)
```

### A* Search
Menggabungkan cost aktual dan estimasi. Menjamin solusi optimal
dan lebih efisien dari UCS jika heuristik admissible.

```
f(n) = g(n) + h(n)
```

---

## Heuristik

| Kode | Nama | Formula | Admissible |
|------|------|---------|------------|
| H1 | Manhattan | `|delta_row| + |delta_col|` | Ya |
| H2 | Chebyshev | `max(|delta_row|, |delta_col|)` | Ya |
| H3 | Euclidean | `sqrt(delta_row^2 + delta_col^2)` | Ya |

Semua heuristik bersifat admissible karena tidak pernah melebih-lebihkan
jarak sebenarnya ke titik tujuan.

---

## Perbandingan Algoritma

| Algoritma | Optimal | Kecepatan | Node Dieksplorasi |
|-----------|---------|-----------|-------------------|
| UCS | Ya (selalu) | Lambat | Sangat banyak |
| GBFS | Tidak | Cepat | Sedikit |
| A* | Ya (jika h admissible) | Seimbang | Sedang |

---

## Author

| NIM | Nama |
|-----|------|
| 13524113 | Fauzan Mohamad Abdul Ghani |
| 13524147 | Muh. Hartawan Haidir |

Program Studi Teknik Informatika
Sekolah Teknik Elektro dan Informatika
Institut Teknologi Bandung
2026