"""
Laboratory Work No. 4 - Task 2
Title: Text Analysis with Regular Expressions
Version: 1.0
Developer: Maleeva Kira 453501
Date: 2026-05-06
"""

from text_analyzer import TextAnalyzer
from file_handler import FileHandler
from regex_processor import RegexProcessor

def create_sample_input():
    """Create sample input file for testing"""
    sample_text = """Hello world! How are you today? This is a test text.
    Buy this product for 23.78 USD or 100 RUR. Also available for 50.5 EU.
    Check this smiley: :-) and this one: ;----[[[[[. Also :(( and ;-).
    Words with letters: fox, yellow, zebra, apple. Apple ends with a.
    Short words: a, an, the. Long words: extraordinary, unbelievable.
    Invalid price: 22 UDD, 0.002 USD.
    """
    
    with open('input.txt', 'w', encoding='utf-8') as f:
        f.write(sample_text)
    print("Sample input.txt created")

def format_results(analyzer: TextAnalyzer) -> str:
    """Format analysis results as string"""
    results = []
    
    # Sentence analysis
    sent_stats = analyzer.count_sentences()
    results.append(f"Total sentences: {sent_stats['total']}")
    results.append(f"Declarative (.): {sent_stats['declarative']}")
    results.append(f"Interrogative (?): {sent_stats['interrogative']}")
    results.append(f"Imperative (!): {sent_stats['imperative']}")
    
    # Length statistics
    results.append(f"Average sentence length (chars): {analyzer.avg_sentence_length()}")
    results.append(f"Average word length (chars): {analyzer.avg_word_length()}")
    
    # Smileys
    results.append(f"\nSmiley count: {analyzer.count_smileys()}")
    
    # Words with letters f-y
    words_f_y = analyzer.find_words_with_letters_f_to_y()
    results.append(f"\nWords containing letters f-y:")
    results.append(f"{', '.join(words_f_y[:10])}")  # Show first 10
    
    # Prices
    prices = analyzer.extract_prices()
    results.append(f"\nPrices extracted:")
    for currency, price_list in prices.items():
        if price_list:
            results.append(f"{currency}: {', '.join(price_list)}")
    
    # Short words
    results.append(f"\nWords shorter than 7 characters: {analyzer.count_short_words()}")
    
    # Shortest word ending with 'a'
    results.append(f"\nShortest word ending with 'a': {analyzer.shortest_word_ending_with_a()}")
    
    # Words sorted by length
    sorted_words = analyzer.sort_words_by_length_desc()
    results.append(f"\nWords sorted by length (descending):")
    results.append(f"{', '.join(sorted_words[:15])}")  # Show first 15
    
    return "\n".join(results)

def main():  
    # Create sample input if not exists
    import os
    if not os.path.exists('input.txt'):
        create_sample_input()
    
    try:
        # Read input file
        text = FileHandler.read_file('input.txt')
        
        # Analyze text
        analyzer = TextAnalyzer(text)
        
        # Get formatted results
        results = format_results(analyzer)
        
        # Display results
        print("\n" + results)
        
        # Save results to file
        FileHandler.save_results('results.txt', results)
        
        # Create zip archive
        zip_info = FileHandler.create_zip('results.txt', 'results.zip')
        print(f"\nCreated archive: {zip_info['filename']}")
        print(f"  Original size: {zip_info['file_size']} bytes")
        print(f"  Compressed size: {zip_info['compressed_size']} bytes")
        print(f"  Compression ratio: {zip_info['compression_ratio']}%")
        
        # Allow repetition
        while True:
            again = input("\nAnalyze another file? (y/n): ").strip().lower()
            if again == 'y':
                filename = input("Enter filename: ").strip()
                try:
                    new_text = FileHandler.read_file(filename)
                    new_analyzer = TextAnalyzer(new_text)
                    new_results = format_results(new_analyzer)
                    print("\n" + new_results)
                    FileHandler.save_results('results_new.txt', new_results)
                except Exception as e:
                    print(f"Error: {e}")
            elif again == 'n':
                break
            else:
                print("Please enter y or n")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()