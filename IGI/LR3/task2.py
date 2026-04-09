"""
Program to count odd natural numbers from user input sequence.
Lab Work 3, Task 2, Variant 17
Version: 1.0
Developer: Maleeva K.A.
Date: 2026-04-09
"""

import ui


def odd_count():
    """
    Count odd natural numbers from user input.
    Stops when user enters 0.
    Returns:
        int: Count of odd natural numbers
    """
    count = 0
    while True:
        num = ui.read_int("Enter an integer (0 to stop): ")
        if num == 0:
            break
        if num > 0 and num % 2 == 1:
            count += 1
    return count


def main():
    """Main function."""
    while True:
        try:
            result = odd_count()
            print(f"\nTotal odd natural numbers entered: {result}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        print()
        if not ui.confirm("Count again? (y/n): "):
            break


if __name__ == "__main__":
    main()