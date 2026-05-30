# Code Explained — Tic Tac Toe

A plain-English walkthrough of every part of `game.py`.

---

## Dependencies

### `pygame`
The only external library used. It handles:
- Opening a window
- Drawing shapes (lines, circles, rectangles)
- Rendering text
- Listening for mouse clicks and keyboard events

Install it with:
```bash
pip install pygame
```

### `sys`
A built-in Python module. Used only for `sys.exit()` — cleanly closes the program when the window is shut.

---

## Constants (Top of the file)

These are fixed values that control the look of the game. Changing them reshapes the whole UI.

```python
WIDTH, HEIGHT = 600, 700
```
The window is 600px wide and 700px tall.  
The extra 100px at the bottom (700 - 600) is the status bar (scores + button).

```python
CELL_SIZE = WIDTH // 3   # = 200px per cell
```
The board is split into 3 equal columns, so each cell is 200×200px.

```python
LINE_WIDTH = 8    # thickness of grid lines
MARK_WIDTH = 12   # thickness of X lines and O circle border
MARK_PADDING = 40 # gap between cell edge and the X or O mark
FPS = 60          # screen refreshes 60 times per second
```

### Colors
All colors are RGB tuples `(Red, Green, Blue)`, each value from 0–255.

| Name      | Value             | Used for              |
|-----------|-------------------|-----------------------|
| `BG`      | (245, 245, 245)   | Background (off-white)|
| `LINE_C`  | (50, 50, 50)      | Grid lines (dark gray)|
| `X_COLOR` | (220, 70, 70)     | X marks (red)         |
| `O_COLOR` | (70, 130, 210)    | O marks (blue)        |
| `WIN_C`   | (80, 200, 120)    | Winning cells (green) |
| `BTN_C`   | (70, 130, 210)    | Button normal state   |
| `BTN_H`   | (50, 110, 190)    | Button hover state    |

---

## Global State Variables

These variables track everything that changes during the game.

```python
board = [""] * 9
```
A list of 9 strings. Empty string = empty cell. `"X"` or `"O"` = taken cell.

```python
current_player = "X"
```
Whose turn it is. Starts as X, switches after every valid move.

```python
game_over = False
```
Becomes `True` once someone wins or it's a draw. Blocks further clicks.

```python
winner = None
```
Stores `"X"`, `"O"`, or `"Draw"` once the game ends.

```python
winning_combo = []
```
Stores the 3 board indexes that formed the winning line (e.g. `[0, 1, 2]`). Used to highlight those cells green.

```python
scores = {"X": 0, "O": 0, "Draw": 0}
```
Keeps running totals across multiple games in the same session.

---

## Functions

---

### `reset_board()`

```python
def reset_board():
    global board, current_player, game_over, winner, winning_combo
    board = [""] * 9
    current_player = "X"
    game_over = False
    winner = None
    winning_combo = []
```

Resets everything back to a fresh game. Does **not** reset scores — those persist until the app closes.

Called when the player clicks the **New Game** button.

---

### `check_winner()`

```python
def check_winner():
    combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],   # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],   # columns
        [0, 4, 8], [2, 4, 6],              # diagonals
    ]
    for combo in combos:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], combo
    if all(cell != "" for cell in board):
        return "Draw", []
    return None, []
```

Checks all 8 winning lines after each move.

- If 3 cells in a combo all hold the same mark → return that mark + the winning combo.
- If all 9 cells are filled but no winner → return `"Draw"`.
- Otherwise → return `None` (game still going).

---

### `draw_grid()`

```python
def draw_grid():
    screen.fill(BG)
    for i in (1, 2):
        y = i * CELL_SIZE
        pygame.draw.line(screen, LINE_C, (20, y), (WIDTH - 20, y), LINE_WIDTH)
    for i in (1, 2):
        x = i * CELL_SIZE
        pygame.draw.line(screen, LINE_C, (x, 20), (x, WIDTH - 20), LINE_WIDTH)
```

- Fills the entire screen with the background color.
- Draws 2 horizontal lines at y=200 and y=400.
- Draws 2 vertical lines at x=200 and x=400.
- The `20px` insets keep the lines from touching the window edges — a small visual style choice.

---

### `draw_marks()`

```python
def draw_marks():
    for i, cell in enumerate(board):
        row, col = divmod(i, 3)
        cx = col * CELL_SIZE + CELL_SIZE // 2
        cy = row * CELL_SIZE + CELL_SIZE // 2
        ...
```

Loops over all 9 cells. For each filled cell:

- `divmod(i, 3)` splits the index into a row and column.  
  Example: index 5 → row 1, col 2.
- `cx` and `cy` are the **center pixel** of that cell.
- **X** is drawn as two diagonal lines crossing through the center.
- **O** is drawn as a circle outline around the center.
- If the cell is part of `winning_combo`, the color switches to green (`WIN_C`).

---

### `draw_status_bar()`

Draws the black bar at the bottom of the screen containing:

1. **Game status** — either whose turn it is, or the winner/draw message.
2. **Score line** — `X: 2   Draw: 1   O: 1`
3. **New Game button** — a blue rectangle that changes shade when the mouse hovers over it.

Returns `btn_rect` (the button's rectangle object) so the main loop can check if it was clicked.

**Hover effect:**
```python
mouse = pygame.mouse.get_pos()
btn_color = BTN_H if btn_rect.collidepoint(mouse) else BTN_C
```
Every frame, it checks if the mouse is over the button and picks the darker hover color if so.

---

### `handle_click(pos)`

```python
def handle_click(pos):
    x, y = pos
    if y >= WIDTH or game_over:
        return None

    col = x // CELL_SIZE
    row = y // CELL_SIZE
    idx = row * 3 + col

    if board[idx] != "":
        return None

    board[idx] = current_player
    w, combo = check_winner()
    ...
```

Called when the player left-clicks inside the grid area.

1. Ignores clicks below the grid (y ≥ 600) and clicks when game is over.
2. Converts pixel coordinates to a grid index:
   - `col = x // 200` → which column (0, 1, or 2)
   - `row = y // 200` → which row (0, 1, or 2)
   - `idx = row * 3 + col` → flat board index (0–8)
3. Ignores clicks on already-filled cells.
4. Places the current player's mark, then checks for a winner.
5. If no winner, flips the current player.

---

### `main()`

```python
def main():
    running = True
    while running:
        btn_rect = draw_grid()
        draw_marks()
        btn_rect = draw_status_bar()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if btn_rect.collidepoint(mx, my):
                    reset_board()
                elif my < WIDTH:
                    handle_click(event.pos)

        clock.tick(FPS)
```

The **game loop** — this runs continuously until the window is closed.

Each frame it:
1. Redraws the grid, marks, and status bar.
2. Calls `pygame.display.flip()` to push the drawn frame to the screen.
3. Processes all events (window close, mouse click).
4. Sleeps just long enough to maintain 60 FPS via `clock.tick(60)`.

`pygame.QUIT` fires when the user clicks the ✕ button — setting `running = False` exits the loop.  
`pygame.MOUSEBUTTONDOWN` fires on any mouse button press — `event.button == 1` filters for left-click only.

---

## Data Flow Summary

```
User clicks
    ↓
handle_click()
    → writes to board[]
    → calls check_winner()
        → returns winner or None
    → updates game_over, winner, winning_combo, scores
    → switches current_player

Every frame (60/sec)
    → draw_grid()       clears screen, draws lines
    → draw_marks()      reads board[], draws X's and O's
    → draw_status_bar() reads game_over, winner, scores, current_player
    → display.flip()    shows the frame
```

All game state lives in the global variables at the top. Every draw function reads those variables — nothing is stored inside the drawing functions themselves.
