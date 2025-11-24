from src.model.student import Student

class AttendancePolicy:
    def check(self, student: Student) -> bool:
        return student.has_reached_minimum_classes

class ExtraPointsPolicy:
    def check(self, student: Student) -> bool:
        return student.has_extra_points_agreement
