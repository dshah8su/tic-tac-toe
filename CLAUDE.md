# Tic Tac Toe — Project Reference for Claude

## Project Overview
A two-player Tic Tac Toe game built in two versions:
- **Desktop version** (`game.py`) — Python + Pygame, runs locally on Windows
- **Web version** (`index.html`) — Pure HTML/CSS/JavaScript, hosted on GitHub Pages

## Live URL
https://dshah8su.github.io/tic-tac-toe/

## GitHub Repository
https://github.com/dshah8su/tic-tac-toe

## Local Project Path
`C:/Users/shahd/Desktop/tic-tac-toe/`

---

## Project Structure

```
tic-tac-toe/
├── game.py            # Desktop game (Python + Pygame)
├── index.html         # Web game (HTML/CSS/JS) — served by GitHub Pages
├── requirements.txt   # Python dependencies (pygame==2.6.1)
├── run.bat            # Double-click launcher for desktop version
├── .gitignore         # Excludes venv/, __pycache__, .pyc files
├── README.md          # User-facing guide and game logic explanation
├── CODE_EXPLAINED.md  # Full line-by-line code walkthrough
├── CLAUDE.md          # This file
└── venv/              # Python virtual environment (not committed to git)
```

---

## Dependencies

### Desktop Version
| Package  | Version | Purpose                            |
|----------|---------|------------------------------------|
| pygame   | 2.6.1   | Window, drawing, input, game loop  |
| sys      | built-in| Clean app exit via sys.exit()      |

### Web Version
No dependencies. Pure browser-native HTML/CSS/JavaScript.

---

## Running the Desktop Version

```bash
# From the project folder
venv\Scripts\activate
python game.py
```

Or double-click `run.bat`.

### Setting up from scratch (after cloning)
```bash
git clone https://github.com/dshah8su/tic-tac-toe
cd tic-tac-toe
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python game.py
```

Python used: `C:/Users/shahd/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe` (Python 3.12.13)

---

## Architecture

### Desktop (`game.py`)

**State variables (globals)**
| Variable         | Type       | Purpose                                      |
|------------------|------------|----------------------------------------------|
| `board`          | list[str]  | 9-element flat list, `""` / `"X"` / `"O"`   |
| `current_player` | str        | Whose turn it is — `"X"` or `"O"`           |
| `game_over`      | bool       | Blocks input once game ends                  |
| `winner`         | str / None | `"X"`, `"O"`, `"Draw"`, or `None`           |
| `winning_combo`  | list[int]  | 3 board indexes forming the winning line     |
| `scores`         | dict       | `{"X": 0, "O": 0, "Draw": 0}`               |

**Functions**
| Function           | Purpose                                                  |
|--------------------|----------------------------------------------------------|
| `reset_board()`    | Clears board state, keeps scores                         |
| `check_winner()`   | Checks all 8 win combos, returns winner + combo or None  |
| `draw_grid()`      | Clears screen, draws the 2×2 grid lines                  |
| `draw_marks()`     | Draws X/O marks; highlights winning cells green          |
| `draw_status_bar()`| Draws score, turn/result text, New Game button           |
| `handle_click(pos)`| Converts pixel click → board index → places mark        |
| `main()`           | 60 FPS game loop: draw → events → tick                   |

**Win detection — 8 combinations checked every move:**
```
Rows:      [0,1,2]  [3,4,5]  [6,7,8]
Columns:   [0,3,6]  [1,4,7]  [2,5,8]
Diagonals: [0,4,8]  [2,4,6]
```

**Click → board index formula:**
```python
col = x // 200
row = y // 200
idx = row * 3 + col
```

### Web (`index.html`)
Self-contained single file. Same game logic re-implemented in JavaScript.
- Board state: `Array(9).fill("")`
- Same 8 win combos checked via `WINS` constant
- Score persists in JS object `{ X: 0, O: 0, Draw: 0 }` for the browser session
- Winning cells highlighted with `.win-cell` CSS class (green background)
- Deployed via GitHub Pages from `master` branch root `/`

---

## Git & Deployment

- Branch: `master`
- GitHub Pages: enabled on `master` branch, root path `/`
- `index.html` at repo root is automatically served as the Pages entry point
- `venv/` is excluded via `.gitignore`

### Push workflow
```bash
git add .
git commit -m "your message"
git push
```
GitHub Pages auto-redeploys within ~1 minute of every push to master.

---

## Design Decisions
- Desktop version uses Pygame (not tkinter) so it has a real dependency to demonstrate virtual environment usage
- Web version is a single `index.html` with no build step or framework — keeps deployment simple (GitHub Pages serves it directly)
- Scores are session-only (not persisted to disk/localStorage) — intentional simplicity
- Window size: 600×700px — 600px for the 3×3 grid (200px per cell), 100px for the status bar
