# automatic predefined movement sequence
import time

def move_forward(time):
    # TODO
    
    time.sleep(time)
    stop(1)
    return

def move_backward(time):
    # TODO

    time.sleep(time)
    stop(1)
    return

def move_left(time):
    # TODO

    time.sleep(time)
    stop(1)
    return

def move_right(time):
    # TODO

    time.sleep(time)
    stop(1)
    return

def stop(time):
    # TODO
    time.sleep(time)
    return

def main():
    while True:
        move_forward(3)
        move_backward(3)
        move_left(3)
        move_right(3)
        stop(3)

if __name__ == '__main__':
    main()