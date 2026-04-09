import random


def gen_init(size):
    """Initialize with random numbers from -10 to 10."""
    return [float(random.randint(-10, 10)) for _ in range(size)]


def user_init(size):
    """Initialize with user input."""
    result = []
    print(f"Enter {size} integers:")
    for i in range(size):
        while True:
            try:
                val = int(input(f"  Element [{i}]: "))
                result.append(float(val))
                break
            except ValueError:
                print("    Invalid input. Enter an integer.")
    return result