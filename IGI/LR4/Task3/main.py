"""
Laboratory Work No. 4 - Task 3
Title: Statistical Analysis of User Input Sequence
Version: 1.0
Developer: Maleeva K.A.
Date: 2026-05-08
"""

import ui
import math
from statistics import SequenceStatistics
from math_series import CosSeries
from plotter import FunctionPlotter


def get_sequence_from_user():
    """
    Get sequence of numbers from user input.
    Uses the same logic as Lab Work 3 (enter numbers until 0).
    
    Returns:
        tuple: (sequence_list, odd_count)
    """
    numbers = []
    odd_count = 0
    
    print("\nEnter integers (0 to stop):")
    
    while True:
        num = ui.read_int("> ")
        if num == 0:
            break
        numbers.append(num)
        if num > 0 and num % 2 == 1:
            odd_count += 1
    
    return numbers, odd_count


def print_statistics(sequence):
    """
    Calculate and display statistical parameters for the sequence.
    """    
    print(f"\nAnalyzed sequence: {sequence}")
    
    stats = SequenceStatistics.get_all(sequence)
    
    print(f"Mean: {stats['mean']}")
    print(f"Median: {stats['median']}")
    print(f"Mode: {stats['mode'] if stats['mode'] else 'no mode'}")
    print(f"Variance: {stats['variance']}")
    print(f"Standard deviation: {stats['std']}")
    print(f"Minimum: {stats['min']}")
    print(f"Maximum: {stats['max']}")
    print(f"Count: {stats['count']}")


def demonstrate_taylor_series():
    """
    Plot cos(x) Taylor series vs math.cos(x)
    """  
    series = CosSeries()
    
    # Generate data for plotting
    x_start = -2 * math.pi
    x_end = 2 * math.pi
    num_points = 200
    terms_list = [1, 2, 3, 4, 6]
    
    data = series.generate_plot_data(x_start, x_end, num_points, terms_list)
    
    # Create plot
    plotter = FunctionPlotter()
    plotter.setup_plot(x_start, x_end)
    plotter.plot_comparison(data)
    plotter.add_legend()
    plotter.add_annotations()
    
    # Part c: Save to file
    plotter.save_plot('cos_series_plot.png')
    
    plotter.show_plot()
    
    plotter.close()


def main():
    """Main function - integrates Lab Work 3 with new statistical analysis.""" 
    while True:
        # Get sequence (exactly as in Lab Work 3)
        sequence, odd_count = get_sequence_from_user()
        
        if not sequence:
            print("No numbers entered.")
            if not ui.confirm("Try again? (y/n): "):
                break
            continue
        
        print(f"\nTotal odd natural numbers: {odd_count}")
        
        print_statistics(sequence)
        
        # Part b and c: Taylor series plot
        demonstrate_taylor_series()
        
        # Ask to repeat
        print()
        if not ui.confirm("Analyze another sequence? (y/n): "):
            break


if __name__ == "__main__":
    main()