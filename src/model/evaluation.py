class Evaluation:
    def __init__(self, grade: float, weight: float):
        if not (0 <= grade <= 20):
            raise ValueError("Grade must be between 0 and 20")
        if not (0 <= weight <= 1):
            raise ValueError("Weight must be between 0 and 1")
        
        self.grade = grade
        self.weight = weight
