from src.model.student import Student
from src.logic.policies import AttendancePolicy, ExtraPointsPolicy

class GradeCalculator:
    def __init__(self):
        self.attendance_policy = AttendancePolicy()
        self.extra_points_policy = ExtraPointsPolicy()
        self.EXTRA_POINTS_VALUE = 1.0
        self.MAX_GRADE_NO_ATTENDANCE = 10.0

    def calculate_final_grade(self, student: Student) -> float:
        detail = self.get_calculation_detail(student)
        return detail['final_grade']

    def get_calculation_detail(self, student: Student) -> dict:
        if not student.evaluations:
            return {
                'average': 0.0,
                'penalty': 0.0,
                'extra_points': 0.0,
                'final_grade': 0.0
            }

        # Calculate weighted average
        total_weight = sum(e.weight for e in student.evaluations)
        if total_weight == 0:
             weighted_sum = 0
        else:
            # Normalize weights if they don't sum to 1? 
            # The requirement says "porcentaje de peso sobre la nota final".
            # Usually weights sum to 1 (100%). If not, we might need to handle it.
            # RNF02 says "pesos inválidos" in edge cases.
            # I will assume we calculate based on the weights provided. 
            # If they sum to < 1, the grade is lower. If > 1, it might be higher (capped at 20).
            # Let's just do sum(grade * weight).
            weighted_sum = sum(e.grade * e.weight for e in student.evaluations)
        
        average = weighted_sum

        # Apply Extra Points
        extra_points = 0.0
        if self.extra_points_policy.check(student):
            extra_points = self.EXTRA_POINTS_VALUE
        
        # Apply Penalty
        penalty = 0.0
        current_grade = average + extra_points
        
        if not self.attendance_policy.check(student):
            # If attendance not met, grade is capped at MAX_GRADE_NO_ATTENDANCE
            if current_grade > self.MAX_GRADE_NO_ATTENDANCE:
                penalty = current_grade - self.MAX_GRADE_NO_ATTENDANCE
        
        final_grade = current_grade - penalty
        
        # Cap at 20 and floor at 0
        final_grade = max(0.0, min(20.0, final_grade))

        return {
            'average': round(average, 2),
            'penalty': round(penalty, 2),
            'extra_points': round(extra_points, 2),
            'final_grade': round(final_grade, 2)
        }
