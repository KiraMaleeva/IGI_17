"""
Laboratory Work No. 4 - Task 1
Title: Working with files, serialization (CSV and Pickle)
Version: 1.0
Developer: Maleeva Kira 453501
Date: 2026-05-06
"""

from student import Student
from csv_serializer import CSVSerializer
from pickle_serializer import PickleSerializer

def input_students():
    """Function to input student data from user"""
    students = []
    while True:
        try:
            last_name = input("Enter last name (or 'stop' to finish): ").strip()
            if last_name.lower() == 'stop':
                break
            day = int(input("Birth day: "))
            month = int(input("Birth month (1-12): "))
            year = int(input("Birth year: "))
            students.append(Student(last_name, day, month, year))
        except ValueError as e:
            print(f"Invalid input: {e}")
    return students

def filter_by_month(students, month):
    """Filter students born in given month"""
    return [s for s in students if s.birth_month == month]

def main():
    # Sample data
    sample_students = [
        Student("Ivanov A.A.", 15, 5, 2010),
        Student("Petrov B.B.", 20, 3, 2011),
        Student("Sidorov C.C.", 10, 5, 2009),
        Student("Kuznetsov D.D.", 5, 12, 2010),
    ]
    
    # 1. CSV serialization
    CSVSerializer.save(sample_students, "students.csv")
    students_csv = CSVSerializer.load("students.csv")
    
    # 2. Pickle serialization
    PickleSerializer.save(sample_students, "students.pkl")
    students_pkl = PickleSerializer.load("students.pkl")
    
    # Search by month
    try:
        month = int(input("Enter birth month to search (1-12): "))
        if not 1 <= month <= 12:
            raise ValueError
    except ValueError:
        print("Invalid month. Using current month.")
        from datetime import datetime
        month = datetime.now().month
    
    filtered = filter_by_month(students_csv, month)
    
    print(f"\nStudents born in month {month}:")
    for s in filtered:
        print(f"  {s}")
    
    # Allow repeat
    while True:
        again = input("\nSearch again? (y/n): ").strip().lower()
        if again == 'y':
            month = int(input("Enter month: "))
            filtered = filter_by_month(students_csv, month)
            for s in filtered:
                print(f"  {s}")
        elif again == 'n':
            break
        else:
            print("Please enter y or n")

if __name__ == "__main__":
    main()