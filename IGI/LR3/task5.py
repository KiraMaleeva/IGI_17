"""
Program to process integer list.
Lab Work 3, Task 5, Variant 17
Version: 1.0
Developer: Maleeva K.A.
Date: 2026-04-09
"""

import ui
import seq_init


def print_list(lst, title="Current list"):
    """Display list on screen."""
    print(f"\n{title}:")
    print("[" + ", ".join([f"{x:g}" for x in lst]) + "]")


def prod_ee(lst):
    """Product of absolute values of even elements at even indices."""
    product = 1
    found = False
    for i in range(0, len(lst), 2):
        if int(lst[i]) % 2 == 0:
            product *= abs(lst[i])
            found = True
    return product if found else 0


def btw_sum(lst):
    """Sum of elements between first and last non-zero elements."""
    first = -1
    last = -1
    for i in range(len(lst)):
        if lst[i] != 0:
            first = i
            break
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] != 0:
            last = i
            break
    if first == -1 or last == -1 or first == last:
        return 0
    total = 0
    for i in range(first + 1, last):
        total += lst[i]
    return total


def main():   
    while True:
        try:
            size = ui.read_int("Enter list size: ", min=1)
            
            print("\nInitialization methods:")
            print("  1. Generator (random -10..10)")
            print("  2. User input")
            method = ui.read_int("Choose (1 or 2): ", min=1, max=2)

            if method == 1:
                lst = seq_init.gen_init(size)
            else:
                lst = seq_init.user_init(size)
            
            print_list(lst, "Original list")
            
            product = prod_ee(lst)
            if product == 0:
                print("\nNo even elements at even indices")
            else:
                print(f"\nProduct: {product:.0f}")
            
            total = btw_sum(lst)
            if total == 0:
                print("No elements between first and last non-zero")
            else:
                print(f"Sum between non-zero: {total:.0f}")
            
            
        except Exception as e:
            print(f"Error: {e}")
        
        print()
        if not ui.confirm("Another list? (y/n): "):
            break


if __name__ == "__main__":
    main()