"""
Program to analyze text: words starting with vowels, double letters, alphabetical order.
Lab Work 3, Task 3, Variant 17
Version: 1.0
Developer: Maleeva K.A.
Date: 2026-04-09
"""

import ui


TEXT = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."


def get_words(text):
    """
    Split text into words (separators: space and comma).
    Args:
        text: Input string
    Returns:
        list: List of words (lowercase, without punctuation)
    """
    text = text.replace(',', ' ')
    words = text.split()
    words = [w.lower() for w in words if w]
    return words


def is_vowel(char):
    """Check if character is a vowel."""
    vowels = 'aeiou'
    return char in vowels


def has_double(word):
    """
    Check if word contains two identical letters in a row.
    Args:
        word: String to check
    Returns:
        bool: True if double letters found
    """
    for i in range(len(word) - 1):
        if word[i] == word[i + 1]:
            return True
    return False


def analyze(text):
    """
    Analyze text according to variant requirements.
    Returns:
        tuple: (vowel_words, double_letter_words, sorted_words)
    """
    words = get_words(text)

    vowel_words = [w for w in words if is_vowel(w[0])]

    double_letter_words = []
    for i, word in enumerate(words, 1):
        if has_double(word):
            double_letter_words.append((i, word))

    sorted_words = sorted(words)

    return vowel_words, double_letter_words, sorted_words


def main():
    """Main function."""    
    print("\nOriginal text:")
    print(f"\"{TEXT}\"")
    
    vowel_words, double_words, sorted_words = analyze(TEXT)
    
    # a) Words starting with vowel
    print(f"\na) Words starting with vowel: {len(vowel_words)}")
    
    # b) Words with double letters
    print(f"\nb) Words with double letters:")
    if double_words:
        for pos, word in double_words:
            print(f"   Position {pos}: \"{word}\"")
    else:
        print("   No words with double letters found")
    
    # c) Words in alphabetical order
    print(f"\nc) All words in alphabetical order:")

    for i in range(0, len(sorted_words), 5):
        print("   " + ", ".join(sorted_words[i:i+5]))


if __name__ == "__main__":
    main()