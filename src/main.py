import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.model.student import Student
from src.model.evaluation import Evaluation
from src.logic.grade_calculator import GradeCalculator

def main():
    print("--- CS-GradeCalculator ---")
    name = input("Enter student name: ")
    student = Student(name)

    print("\n--- Register Evaluations ---")
    while True:
        try:
            grade_input = input("Enter grade (0-20) or 'q' to finish: ")
            if grade_input.lower() == 'q':
                break
            grade = float(grade_input)
            
            weight_input = input("Enter weight (0-1, e.g., 0.2 for 20%): ")
            weight = float(weight_input)
            
            evaluation = Evaluation(grade, weight)
            student.add_evaluation(evaluation)
            print("Evaluation added.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    print("\n--- Attendance ---")
    attendance_input = input("Has the student reached minimum classes? (y/n): ")
    student.has_reached_minimum_classes = attendance_input.lower() == 'y'

    print("\n--- Extra Points ---")
    extra_input = input("Is there an agreement for extra points? (y/n): ")
    student.has_extra_points_agreement = extra_input.lower() == 'y'

    calculator = GradeCalculator()
    detail = calculator.get_calculation_detail(student)

    print("\n--- Calculation Result ---")
    print(f"Student: {student.name}")
    print(f"Weighted Average: {detail['average']}")
    print(f"Extra Points: {detail['extra_points']}")
    print(f"Penalty (Attendance): {detail['penalty']}")
    print(f"Final Grade: {detail['final_grade']}")

if __name__ == "__main__":
    main()
