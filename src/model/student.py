from typing import List
from src.model.evaluation import Evaluation

class Student:
    def __init__(self, name: str):
        self.name = name
        self.evaluations: List[Evaluation] = []
        self.has_reached_minimum_classes = False
        self.has_extra_points_agreement = False

    def add_evaluation(self, evaluation: Evaluation):
        if len(self.evaluations) >= 10:
            raise ValueError("Maximum number of evaluations reached (10)")
        self.evaluations.append(evaluation)
