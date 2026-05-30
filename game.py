import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 700
LINE_WIDTH = 8
CELL_SIZE = WIDTH // 3
MARK_WIDTH = 12
MARK_PADDING = 40
FPS = 60

WHITE   = (255, 255, 255)
BLACK   = (20, 20, 20)
BG      = (245, 245, 245)
LINE_C  = (50, 50, 50)
X_COLOR = (220, 70, 70)
O_COLOR = (70, 130, 210)
WIN_C   = (80, 200, 120)
BTN_C   = (70, 130, 210)
BTN_H   = (50, 110, 190)
GRAY    = (150, 150, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

font_large  = pygame.font.SysFont("segoeui", 56, bold=True)
font_medium = pygame.font.SysFont("segoeui", 32)
font_small  = pygame.font.SysFont("segoeui", 24)

board = [""] * 9
current_player = "X"
game_over = False
winner = None
winning_combo = []
scores = {"X": 0, "O": 0, "Draw": 0}


def reset_board():
    global board, current_player, game_over, winner, winning_combo
    board = [""] * 9
    current_player = "X"
    game_over = False
    winner = None
    winning_combo = []


def check_winner():
    combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6],
    ]
    for combo in combos:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], combo
    if all(cell != "" for cell in board):
        return "Draw", []
    return None, []


def draw_grid():
    screen.fill(BG)
    # horizontal lines
    for i in (1, 2):
        y = i * CELL_SIZE
        pygame.draw.line(screen, LINE_C, (20, y), (WIDTH - 20, y), LINE_WIDTH)
    # vertical lines
    for i in (1, 2):
        x = i * CELL_SIZE
        pygame.draw.line(screen, LINE_C, (x, 20), (x, WIDTH - 20), LINE_WIDTH)


def draw_marks():
    for i, cell in enumerate(board):
        row, col = divmod(i, 3)
        cx = col * CELL_SIZE + CELL_SIZE // 2
        cy = row * CELL_SIZE + CELL_SIZE // 2
        p = MARK_PADDING
        if cell == "X":
            color = X_COLOR
            if winning_combo and i in winning_combo:
                color = WIN_C
            pygame.draw.line(screen, color,
                             (cx - CELL_SIZE // 2 + p, cy - CELL_SIZE // 2 + p),
                             (cx + CELL_SIZE // 2 - p, cy + CELL_SIZE // 2 - p), MARK_WIDTH)
            pygame.draw.line(screen, color,
                             (cx + CELL_SIZE // 2 - p, cy - CELL_SIZE // 2 + p),
                             (cx - CELL_SIZE // 2 + p, cy + CELL_SIZE // 2 - p), MARK_WIDTH)
        elif cell == "O":
            color = O_COLOR
            if winning_combo and i in winning_combo:
                color = WIN_C
            pygame.draw.circle(screen, color, (cx, cy),
                               CELL_SIZE // 2 - p, MARK_WIDTH)


def draw_status_bar():
    bar_rect = pygame.Rect(0, WIDTH, WIDTH, HEIGHT - WIDTH)
    pygame.draw.rect(screen, BLACK, bar_rect)

    if game_over:
        if winner == "Draw":
            msg = "It's a Draw!"
            color = GRAY
        else:
            msg = f"Player {winner} Wins!"
            color = WIN_C
        text = font_large.render(msg, True, color)
        screen.blit(text, text.get_rect(center=(WIDTH // 2, WIDTH + 35)))
    else:
        turn_txt = font_medium.render(f"Player {current_player}'s Turn", True, WHITE)
        screen.blit(turn_txt, turn_txt.get_rect(center=(WIDTH // 2, WIDTH + 30)))

    score_txt = font_small.render(
        f"X: {scores['X']}   Draw: {scores['Draw']}   O: {scores['O']}",
        True, GRAY
    )
    screen.blit(score_txt, score_txt.get_rect(center=(WIDTH // 2, WIDTH + 65)))

    btn_rect = pygame.Rect(WIDTH // 2 - 70, WIDTH + 82, 140, 40)
    mouse = pygame.mouse.get_pos()
    btn_color = BTN_H if btn_rect.collidepoint(mouse) else BTN_C
    pygame.draw.rect(screen, btn_color, btn_rect, border_radius=8)
    btn_text = font_small.render("New Game", True, WHITE)
    screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))

    return btn_rect


def handle_click(pos):
    global current_player, game_over, winner, winning_combo

    x, y = pos
    if y >= WIDTH:
        return None  # handled by caller

    if game_over:
        return None

    col = x // CELL_SIZE
    row = y // CELL_SIZE
    idx = row * 3 + col

    if board[idx] != "":
        return None

    board[idx] = current_player
    w, combo = check_winner()
    if w:
        game_over = True
        winner = w
        winning_combo = combo
        scores[w] += 1
    else:
        current_player = "O" if current_player == "X" else "X"


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

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
