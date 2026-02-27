# ♟️ Chess Engine

A fully featured chess application built in Python with a native macOS GUI. Designed both for **playing** and for **testing and analysis** — the program supports a complete manual mode, allowing users to set up any position via FEN, play moves freely for both sides, and evaluate positions on demand.

---

## ✨ Features

- **AI engine** with iterative deepening, alpha-beta pruning, and transposition table (Zobrist hashing)
- **Piece-square tables** and mobility evaluation
- **Mate in N detection** with audible warning
- **Animated piece moves** with sound effects
- **Chess clock** — configurable per side, or disabled entirely (unlimited time)
- **Manual / testing mode** — play both sides freely, load any FEN position
- **Best Move highlight** — engine suggests a move with 2-second board highlight
- **Captured pieces** display, updated after every move
- **Move log** with move numbers and check notation
- **Scrollable control panel** — works on any screen size
- **Copy / Import FEN** for position sharing and analysis
- **Native macOS `.app` bundle** — no installation required

---

## 🖥️ Interface

```
┌─────────────────────────┬──────────────────┐
│                         │  Move log        │
│      Chessboard         │  Last move       │
│   (click to move)       │  Clock           │
│                         │  AI stats        │
│                         ├──────────────────│
│                         │  Scrollable      │
│                         │  control panel   │
└─────────────────────────┴──────────────────┘
```

---

## 🚀 Getting Started

### Run from source

```bash
pip install python-chess
python chess_engine_gui_new.py
```

**Requirements:** Python 3.9+, `python-chess`, `tkinter`

> On macOS, if tkinter is missing: `brew install python-tk`

### Build macOS app

```bash
pip install pyinstaller python-chess
pyinstaller ChessEngine.spec
# Result: dist/ChessEngine.app
```

On first launch, macOS may show a Gatekeeper warning — right-click the app and choose **Open**.

---

## 🎮 Controls

### Buttons

| Button | Action |
|--------|--------|
| **AI Move** | Engine plays one move for the side to move |
| **AUTO** | Engine plays continuously — press STOP to halt |
| **STOP** | Stops automatic play |
| **UNDO** | Takes back the last move |
| **RESET** | Returns to starting position, clears all stats |
| **Best Move** | Highlights the best move without playing it (2 sec) |
| **History** | Shows full move history in the info panel |
| **Copy FEN** | Copies current FEN to clipboard |
| **Import FEN** | Loads a position from a FEN string |

### Settings

| Setting | Description |
|---------|-------------|
| **Depth** | Maximum search depth (1–20, default: 4) |
| **Time(s)** | Max thinking time per move in seconds (0.5–300) |
| **Clock** | Minutes per side — set to `0` to disable the clock |

---

## 🧪 Manual & Testing Mode

The engine is fully designed to support manual testing and position analysis:

- Load any position with **Import FEN**
- Play moves for **both White and Black** freely
- Use **Best Move** to inspect the engine's recommendation without committing
- Set **Clock to 0** for untimed analysis
- Use **AI Move** to evaluate specific positions step by step

---

## 📊 Status Display

After each move the right panel shows:

```
1. [W] e2e4  ► Mate in 2!
White: 29:55   Black: 30:00
depth: 4  |  nodes: 0.04MN
TT: 1,975  |  eval: -3.49
```

- `[W]` / `[B]` — side that moved
- `eval` — position evaluation in pawns (positive = White advantage)
- `nodes` — positions searched (in mega-nodes)
- `TT` — transposition table entries

---

## 💻 Terminal Commands

The program also accepts commands in the terminal:

| Command | Action |
|---------|--------|
| `e2e4` | Play move in UCI format |
| `best` | Show best move without playing |
| `h` / `history` | Print move history |
| `b` / `back` | Undo last move |
| `fen` | Print current FEN |
| `dep N` | Set search depth to N |
| `lim N` | Set time limit to N seconds |
| `go` | Start AUTO mode |
| `stop` | Stop AUTO mode |
| `q` | Quit |

---

## 🔊 Sound Effects

All sounds are generated internally via WAV synthesis — no external audio files needed.

| Event | Sound |
|-------|-------|
| Move | Short two-tone click |
| Check | Two-tone alert |
| Checkmate | Four-note fanfare |
| Draw / Stalemate | Descending three-note tone |
| Mate warning | Triple pulse |

---

## 📋 System Requirements

- macOS 10.13 (High Sierra) or later
- Apple Silicon (arm64) and Intel (x86_64) supported
- No installation required when using the `.app` bundle

---

## 📁 Files

| File | Description |
|------|-------------|
| `chess_engine_gui_new.py` | Main application source |
| `ChessEngine.spec` | PyInstaller build config for macOS |
| `README.md` | This file |

---

*Josef@2026*
