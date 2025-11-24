import unittest
from src.model.student import Student
from src.model.evaluation import Evaluation
from src.logic.grade_calculator import GradeCalculator

class TestGradeCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = GradeCalculator()
        self.student = Student("Test Student")

    def test_normal_calculation(self):
        # 50% of 14 + 50% of 16 = 15
        self.student.add_evaluation(Evaluation(14, 0.5))
        self.student.add_evaluation(Evaluation(16, 0.5))
        self.student.has_reached_minimum_classes = True
        
        final_grade = self.calculator.calculate_final_grade(self.student)
        self.assertEqual(final_grade, 15.0)

    def test_attendance_penalty(self):
        # 100% of 15 = 15. No attendance -> Cap at 10. Penalty = 5.
        self.student.add_evaluation(Evaluation(15, 1.0))
        self.student.has_reached_minimum_classes = False
        
        detail = self.calculator.get_calculation_detail(self.student)
        self.assertEqual(detail['final_grade'], 10.0)
        self.assertEqual(detail['penalty'], 5.0)

    def test_attendance_penalty_low_grade(self):
        # 100% of 8 = 8. No attendance -> Cap at 10. Since 8 < 10, no penalty.
        self.student.add_evaluation(Evaluation(8, 1.0))
        self.student.has_reached_minimum_classes = False
        
        detail = self.calculator.get_calculation_detail(self.student)
        self.assertEqual(detail['final_grade'], 8.0)
        self.assertEqual(detail['penalty'], 0.0)

    def test_extra_points(self):
        # 100% of 14 = 14. Extra points = 1. Final = 15.
        self.student.add_evaluation(Evaluation(14, 1.0))
        self.student.has_reached_minimum_classes = True
        self.student.has_extra_points_agreement = True
        
        final_grade = self.calculator.calculate_final_grade(self.student)
        self.assertEqual(final_grade, 15.0)

    def test_edge_case_zero_evaluations(self):
        final_grade = self.calculator.calculate_final_grade(self.student)
        self.assertEqual(final_grade, 0.0)

    def test_edge_case_max_evaluations(self):
        for _ in range(10):
            self.student.add_evaluation(Evaluation(20, 0.1))
        
        with self.assertRaises(ValueError):
            self.student.add_evaluation(Evaluation(20, 0.1))
        
        self.student.has_reached_minimum_classes = True
        final_grade = self.calculator.calculate_final_grade(self.student)
        self.assertAlmostEqual(final_grade, 20.0)

    def test_invalid_weights_sum(self):
        # Weights sum to 0.5. Grade 20. Result 10.
        self.student.add_evaluation(Evaluation(20, 0.5))
        self.student.has_reached_minimum_classes = True
        
        final_grade = self.calculator.calculate_final_grade(self.student)
        self.assertEqual(final_grade, 10.0)

    def test_determinism(self):
        self.student.add_evaluation(Evaluation(15, 1.0))
        self.student.has_reached_minimum_classes = True
        
        grade1 = self.calculator.calculate_final_grade(self.student)
        grade2 = self.calculator.calculate_final_grade(self.student)
        self.assertEqual(grade1, grade2)

if __name__ == '__main__':
    unittest.main()
