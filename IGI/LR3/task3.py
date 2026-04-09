"""
Program to count Latin letters and digits in a string.
Lab Work 3, Task 3, Variant 17
Version: 1.0
Developer: Maleeva K.A.
Date: 2026-04-09
"""

import ui


def count_ld(text):
    """
    Count Latin letters (a-z, A-Z) and digits (0-9) in string.
    Args:
        text: Input string
    Returns:
        tuple: (letters_count, digits_count)
    """
    letters = 0
    digits = 0
    for ch in text:
        if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'):
            letters += 1
        elif '0' <= ch <= '9':
            digits += 1
    return letters, digits


def main():
    """Main function."""  
    while True:
        try:
            text = ui.read_str("Enter a string: ", allow_empty=True)
            
            letters, digits = count_ld(text)
            
            print(f"Latin letters: {letters}")
            print(f"Digits: {digits}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        print()
        if not ui.confirm("Analyze another string? (y/n): "):
            break


if __name__ == "__main__":
    main()