import pickle

class PickleSerializer:
    """Pickle format serializer"""
    
    @staticmethod
    def save(students, filename):
        with open(filename, 'wb') as f:
            pickle.dump(students, f)
    
    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)