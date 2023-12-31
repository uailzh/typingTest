import curses
from curses import wrapper
import time
import random

# Function to display the welcome message and prompt to start the game
def start_game(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

# Function to display the target text, current input, and WPM
def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    # Loop through each character in the current input
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)  # Default: green font color

        # Change font color to red if the typed character is incorrect
        if char != correct_char:
            color = curses.color_pair(2)  # Red font color

        stdscr.addstr(0, i, char, color)

# Function to load a random line of text from the "text.txt" file
def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

# Function to conduct the WPM test
def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)  # Set non-blocking input

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)  # Set blocking input when the target is completed
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # Exit the game if the ESC key is pressed
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()  # Remove the last character on backspace
        elif len(current_text) < len(target_text):
            current_text.append(key)  # Add typed characters to the current input

# Main function
def main(stdscr):
    # Initialize color pairs for text rendering
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Green font on black background
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Red font on black background
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_WHITE)  # White font on white background

    start_game(stdscr)

    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed a game! Press any key to play again")
        key = stdscr.getkey()
        if ord(key) == 27:  # Exit the game if the ESC key is pressed
            break

# Run the main function using the curses wrapper
wrapper(main)
