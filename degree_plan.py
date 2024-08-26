import math

from course import Course
from itertools import chain, combinations


class Semester:
    def __init__(self, courses: frozenset[Course]):
        self.__courses = courses

    @property
    def courses(self) -> frozenset[Course]:
        return self.__courses


class DegreePlan:
    def __init__(self, degree_courses: frozenset[Course], mandatory_courses_points: int, min_points: int,
                 min_semester_points: int = 0, max_semester_points: int = math.inf):
        self.__degree_courses = degree_courses
        self.__mandatory_points_left = mandatory_courses_points
        self.__total_points_left = min_points
        self.__min_semester_points = min_semester_points
        self.__max_semester_points = max_semester_points
        self.__semester_num = 0
        self.__courses_so_far: set[int] = set()

    def add_semester(self, semester: Semester) -> "DegreePlan":
        if not self._is_valid_semester(semester):
            raise ValueError("Semester is not allowed")

        new_degree_plan = self.__copy__()
        new_degree_plan.__semester_num += 1
        for course in semester.courses:
            new_degree_plan.__total_points_left -= course.points
            if course.is_mandatory:
                new_degree_plan.__mandatory_points_left -= course.points
            new_degree_plan.__courses_so_far.add(course.number)
        return new_degree_plan

    def _is_valid_semester(self, semester: Semester) -> bool:
        for course in semester.courses:
            if self._is_invalid_course(course):
                return False
        return True

    def _is_invalid_course(self, course: Course) -> bool:
        return course.number in self.__courses_so_far or not course.can_take_this_course(
            self.__courses_so_far)

    def get_legal_semesters(self) -> list[Semester]:
        legal_courses = filter(self._is_invalid_course, self.__degree_courses)
        legal_course_subsets = chain.from_iterable(
            combinations(legal_courses, r) for r in range(len(legal_courses) + 1))
        legal_course_subsets = filter(
            lambda subset: self.__min_semester_points <= sum(course.points for course in subset) <=
                           self.__max_semester_points, legal_course_subsets)
        return [Semester(frozenset(subset)) for subset in legal_course_subsets]

    # __eq__ and __hash__ functions are needed for graph search when using 'visited' set.
    def __eq__(self, other) -> bool:
        if not isinstance(other, DegreePlan):
            return False
        return (
                self.__mandatory_points_left == other.__mandatory_points_left and
                self.__total_points_left == other.__total_points_left and
                self.__semester_num == other.__semester_num and
                self.__courses_so_far == other.__courses_so_far
        )

    def __hash__(self) -> int:
        return hash((
            self.__mandatory_points_left,
            self.__total_points_left,
            self.__semester_num,
            frozenset(self.__courses_so_far)
        ))

    def __copy__(self):
        new_plan = DegreePlan(self.__degree_courses, self.__mandatory_points_left, self.__total_points_left,
                              self.__min_semester_points, self.__max_semester_points)
        new_plan.__semester_num = self.__semester_num
        new_plan.__courses_so_far = self.__courses_so_far.copy()
        return new_plan
