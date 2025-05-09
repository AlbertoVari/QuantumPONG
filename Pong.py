import curses
import time

# Impostazioni
BALL_CHAR = 'O'
PADDLE_CHAR = '|'
HEIGHT = 20
WIDTH = 60
PADDLE_SIZE = 4

def draw_paddle(win, x, y):
    for i in range(PADDLE_SIZE):
        win.addch(y + i, x, PADDLE_CHAR)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    while True:
        stdscr.clear()

        # Controllo dimensione finestra
        height, width = stdscr.getmaxyx()
        if height < HEIGHT or width < WIDTH:
            stdscr.addstr(0, 0, "Finestra troppo piccola! (min 60x20)")
            stdscr.refresh()
            time.sleep(2)
            return

        # Inizializza posizioni
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_dx, ball_dy = 1, 1

        paddle1_y = HEIGHT // 2 - PADDLE_SIZE // 2
        paddle2_y = HEIGHT // 2 - PADDLE_SIZE // 2
        paddle1_x = 1
        paddle2_x = WIDTH - 2

        break  # esci dal controllo dimensioni

    # Ciclo principale di gioco
    while True:
        stdscr.clear()
        stdscr.border()

        draw_paddle(stdscr, paddle1_x, paddle1_y)
        draw_paddle(stdscr, paddle2_x, paddle2_y)
        stdscr.addch(ball_y, ball_x, BALL_CHAR)

        key = stdscr.getch()

        
        ball_x += ball_dx
        ball_y += ball_dy

        if ball_y <= 1 or ball_y >= HEIGHT - 2:
            ball_dy *= -1

        if ball_x == paddle1_x + 1 and paddle1_y <= ball_y < paddle1_y + PADDLE_SIZE:
            ball_dx *= -1

        if ball_x == paddle2_x - 1 and paddle2_y <= ball_y < paddle2_y + PADDLE_SIZE:
            ball_dx *= -1

        if ball_x <= 0 or ball_x >= WIDTH - 1:
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx *= -1
            ball_dy = 1 if ball_dy > 0 else -1

        stdscr.refresh()
        time.sleep(0.05)

if __name__ == '__main__':
    curses.wrapper(main)
