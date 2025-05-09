
import curses
import time
import random
import pennylane as qml
from pennylane import numpy as np

BALL_CHAR = 'O'
PADDLE_CHAR = '|'
HEIGHT = 20
WIDTH = 60
PADDLE_SIZE = 4
WIN_SCORE = 10

# Quantum uncertainty simulation (with shots)
dev = qml.device("default.qubit", wires=1, shots=1)

@qml.qnode(dev)
def uncertainty_gate():
    qml.Hadamard(wires=0)
    return qml.sample(wires=0)

def quantum_uncertainty():
    result = uncertainty_gate()
    return 1 if result == 1 else -1

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
        last_quantum_time = time.time()

        while True:
            stdscr.clear()
            stdscr.border()

            stdscr.addstr(0, 2, f"Player 1: {score1}   AI: {score2}   (First to {WIN_SCORE})")

            draw_paddle(stdscr, paddle1_x, paddle1_y)
            draw_paddle(stdscr, paddle2_x, paddle2_y)

            current_time = time.time()
            quantum_active = False

            if current_time - last_quantum_time >= 0.2:
                quantum_active = True
                last_quantum_time = current_time

            key = stdscr.getch()

            if key == ord('w') and paddle1_y > 1:
                paddle1_y -= 1
            elif key == ord('s') and paddle1_y < HEIGHT - PADDLE_SIZE - 1:
                paddle1_y += 1

            if frame_count % ai_speed == 0 and ball_dx > 0:
                if random.random() > ai_error_chance:
                    if ball_y < paddle2_y and paddle2_y > 1:
                        paddle2_y -= 1
                    elif ball_y > paddle2_y + PADDLE_SIZE - 1 and paddle2_y < HEIGHT - PADDLE_SIZE - 1:
                        paddle2_y += 1

            if not quantum_active:
              if 1 <= ball_y < HEIGHT - 1 and 1 <= ball_x < WIDTH - 1:
                 stdscr.addch(ball_y, ball_x, BALL_CHAR)

            
            # Check for human momentum boost (spacebar)
            boost_active = False
            boost_start = 0
            if key == ord(' '):
                boost_active = True
                boost_start = time.time()

            # Check for AI momentum boost when ball moves toward player 1
            if ball_dx < 0 and frame_count % ai_speed == 0:
                ai_boost = True
                ai_boost_start = time.time()
            else:
                ai_boost = False

            # Update ball position normally
    
            
            # Apply boost if active (human or AI)
            if boost_active and time.time() - boost_start < 0.4:
                ball_x = max(1, min(WIDTH - 2, ball_x + ball_dx * 2))
            elif ai_boost and time.time() - ai_boost_start < 0.4:
                ball_x = max(1, min(WIDTH - 2, ball_x + ball_dx * 2))
            else:
                ball_x = max(1, min(WIDTH - 2, ball_x + ball_dx))

            
            if boost_active and time.time() - boost_start < 0.4:
                ball_y = max(1, min(HEIGHT - 2, ball_y + ball_dy * 2))
            elif ai_boost and time.time() - ai_boost_start < 0.4:
                ball_y = max(1, min(HEIGHT - 2, ball_y + ball_dy * 2))
            else:
                ball_y = max(1, min(HEIGHT - 2, ball_y + ball_dy))


            # When Hadamard is "applied", let quantum effect randomize direction
            if quantum_active:
                ball_dx *= quantum_uncertainty()
                ball_dy *= quantum_uncertainty()

            if ball_y <= 1 or ball_y >= HEIGHT - 2:
                ball_dy *= -1

            if ball_x == paddle1_x + 1 and paddle1_y <= ball_y < paddle1_y + PADDLE_SIZE:
                ball_dx *= -1

            if ball_x == paddle2_x - 1 and paddle2_y <= ball_y < paddle2_y + PADDLE_SIZE:
                ball_dx *= -1

            if (ball_x <= paddle1_x + 1 and not (paddle1_y <= ball_y < paddle1_y + PADDLE_SIZE)):
                score2 += 1
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                ball_dx = 1
                ball_dy = 1 if random.random() > 0.5 else -1
                time.sleep(1)
                score2 += 1
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                ball_dx = 1
                ball_dy = 1 if random.random() > 0.5 else -1
                time.sleep(1)

            if (ball_x >= paddle2_x - 1 and not (paddle2_y <= ball_y < paddle2_y + PADDLE_SIZE)):
                score1 += 1
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                ball_dx = -1
                ball_dy = 1 if random.random() > 0.5 else -1
                time.sleep(1)
                score1 += 1
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                ball_dx = -1
                ball_dy = 1 if random.random() > 0.5 else -1
                time.sleep(1)

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