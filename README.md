# Tic Tac Toe

A simple two-player Tic Tac Toe game built with Python and Pygame.

---

## How to Play

- Two players take turns: **X goes first**, then **O**.
- Click any empty square to place your mark.
- First player to get **3 in a row** (across, down, or diagonal) wins.
- If all 9 squares fill up with no winner, it's a **Draw**.
- Click **New Game** to reset the board. Scores carry over.

---

## Game Logic — Step by Step

### 1. The Board
The board is a flat list of 9 empty strings:

```
["", "", "", "", "", "", "", "", ""]
```

Think of it as a grid numbered like this:

```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

When a player clicks a cell, their mark (`"X"` or `"O"`) is stored at that index.

---

### 2. Detecting a Win
After every move, the game checks all **8 possible winning lines**:

| Type       | Combinations          |
|------------|-----------------------|
| Rows       | [0,1,2] [3,4,5] [6,7,8] |
| Columns    | [0,3,6] [1,4,7] [2,5,8] |
| Diagonals  | [0,4,8] [2,4,6]       |

For each combination, if all 3 cells hold the same mark → that player wins.  
If all 9 cells are filled and nobody won → it's a Draw.

---

### 3. Handling a Click
When the player clicks the screen:

1. Convert the pixel position (x, y) into a grid column and row.
2. Calculate the board index: `index = row * 3 + col`
3. If that cell is empty, place the current player's mark there.
4. Check for a winner.
5. If no winner yet, switch turns (`X → O` or `O → X`).

---

### 4. The Game Loop
The game runs in a continuous loop at **60 frames per second**:

```
while running:
    draw the grid
    draw X's and O's
    draw the status bar (scores, turn, button)
    check for mouse clicks or window close
```

This loop keeps the screen refreshed and responsive to input at all times.

---

### 5. Winning Highlight
When someone wins, the 3 winning cells turn **green** instead of red/blue so players can clearly see the winning line.

---

### 6. Score Tracking
Scores are kept in memory as long as the app is open:

```python
scores = {"X": 0, "O": 0, "Draw": 0}
```

Each time a game ends, the winner's score increases by 1. Clicking **New Game** only resets the board — scores are preserved.

---

## Project Structure

```
tic-tac-toe/
├── game.py           # All game code
├── requirements.txt  # Python dependencies
├── run.bat           # Double-click to launch on Windows
├── README.md         # This file
├── CODE_EXPLAINED.md # Detailed code walkthrough
└── venv/             # Virtual environment (not committed to git)
```

---

## Running the Game

```bash
# Activate the virtual environment
venv\Scripts\activate

# Run the game
python game.py
```

Or just double-click `run.bat`.
