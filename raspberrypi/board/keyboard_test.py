# import curses

# def main(stdscr):
#     # Clear screen
#     stdscr.clear()
    
#     stdscr.addstr("Press 'q' to exit.\n")
    
#     while True:
#         key = stdscr.getch()
#         if key == ord('q'):
#             break
#         stdscr.addstr(f"You pressed: {chr(key)}\n")
#         stdscr.refresh()

# if __name__ == "__main__":
#     curses.wrapper(main)