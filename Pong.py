import curses
import time
import random

BALL_CHAR = 'O'
PADDLE_CHAR = '|'
HEIGHT = 20
TOP_BOUND = 3
BOTTOM_BOUND = HEIGHT - 4
WIDTH = 60
PADDLE_SIZE = 4
WIN_SCORE = 10

def draw_paddle(win, x, y):
    for i in range(PADDLE_SIZE):
        win.addch(y + i, x, PADDLE_CHAR)

def select_difficulty(stdscr):
    options = ["Easy", "Medium", "Hard"]
    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select AI Difficulty (Use arrow keys, Enter to confirm):")
        for idx, option in enumerate(options):
            if idx == selected:
                stdscr.addstr(2 + idx, 2, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(2 + idx, 2, f"  {option}")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(options) - 1:
            selected += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            return options[selected]

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(0)
    stdscr.keypad(True)
    stdscr.timeout(100)

    difficulty = select_difficulty(stdscr)

    # AI behavior tuning
    if difficulty == "Easy":
        ai_speed = 2
        ai_error_chance = 0.3
    elif difficulty == "Medium":
        ai_speed = 1
        ai_error_chance = 0.1
    else:
        ai_speed = 1
        ai_error_chance = 0.0

    stdscr.nodelay(1)

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        if height < HEIGHT or width < WIDTH:
            stdscr.addstr(0, 0, "Finestra troppo piccola! (min 60x20)")
            stdscr.refresh()
            time.sleep(2)
            return

        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_dx, ball_dy = 1, 1

        paddle1_y = HEIGHT // 2 - PADDLE_SIZE // 2
        paddle2_y = HEIGHT // 2 - PADDLE_SIZE // 2
        paddle1_x = 1
        paddle2_x = WIDTH - 2

        score1 = 0
        score2 = 0
        frame_count = 0

        while True:
            stdscr.clear()
            stdscr.border()

            stdscr.addstr(0, 2, f"Player 1: {score1}   AI: {score2}   (First to {WIN_SCORE})")

            draw_paddle(stdscr, paddle1_x, paddle1_y)
            draw_paddle(stdscr, paddle2_x, paddle2_y)
            stdscr.addch(ball_y, ball_x, BALL_CHAR)

            key = stdscr.getch()

            if key == ord('w') and paddle1_y > 1:
                paddle1_y -= 1
            elif key == ord('s') and paddle1_y < HEIGHT - PADDLE_SIZE - 1:
                paddle1_y += 1

            # AI movement
            if frame_count % ai_speed == 0 and ball_dx > 0:
                if random.random() > ai_error_chance:
                    if ball_y < paddle2_y and paddle2_y > 1:
                        paddle2_y -= 1
                    elif ball_y > paddle2_y + PADDLE_SIZE - 1 and paddle2_y < HEIGHT - PADDLE_SIZE - 1:
                        paddle2_y += 1

            # Ball movement
            ball_x += ball_dx
            ball_y += ball_dy

            if ball_y <= TOP_BOUND or ball_y >= BOTTOM_BOUND:
                ball_dy *= -1

            if ball_x == paddle1_x + 1 and paddle1_y <= ball_y < paddle1_y + PADDLE_SIZE:
                ball_dx *= -1

            if ball_x == paddle2_x - 1 and paddle2_y <= ball_y < paddle2_y + PADDLE_SIZE:
                ball_dx *= -1

            # Scoring
            if ball_x <= 0:
                score2 += 1
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                ball_dx = 1
                ball_dy = 1 if random.random() > 0.5 else -1
                time.sleep(1)

            if ball_x >= WIDTH - 1:
                score1 += 1
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                ball_dx = -1
                ball_dy = 1 if random.random() > 0.5 else -1
                time.sleep(1)

            # Win check
            if score1 >= WIN_SCORE or score2 >= WIN_SCORE:
                stdscr.clear()
                winner = "Player 1" if score1 > score2 else "AI"
                stdscr.addstr(HEIGHT // 2, WIDTH // 2 - 7, f"{winner} Wins!", curses.A_BOLD)
                stdscr.refresh()
                time.sleep(3)
                return

            stdscr.refresh()
            time.sleep(0.05)
            frame_count += 1

if __name__ == '__main__':
    curses.wrapper(main)
