import csv

class CSVSerializer:
    """CSV format serializer"""
    
    @staticmethod
    def save(students, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['last_name', 'day', 'month', 'year'])
            for s in students:
                writer.writerow([s.last_name, s._birth_day, s._birth_month, s._birth_year])
    
    @staticmethod
    def load(filename):
        from student import Student
        students = []
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append(Student(row['last_name'], int(row['day']), int(row['month']), int(row['year'])))
        return students