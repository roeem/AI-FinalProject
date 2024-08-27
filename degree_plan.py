from course import Course
from itertools import chain, combinations


class Semester:
    """
    This class represent a Semester.
    TODO: Now it is just a set of courses - if it stays that way this class will not be necessary.
          If we don't delete this class maybe move it to another file.
    """
    A = 'A'
    B = 'B'

    def __init__(self, courses: frozenset[Course]):
        self.__courses = courses

    @property
    def courses(self) -> frozenset[Course]:
        return self.__courses


class DegreePlan:
    """
    This class represent a Degree Plan.
    This class is immutable and can be used as state in search problem.
    Each Degree Plane (state) contains the requirements for finishing the degree, all courses already
    placed in previous semesters, all courses available fot this degree and more.
    """

    def __init__(self, degree_courses: frozenset[Course], mandatory_courses_points: int,
                 min_degree_points: int, min_semester_points: int, max_semester_points: int):
        """
        :param degree_courses: a frozenset of courses available for this degree
        :param mandatory_courses_points: number of points of mandatory courses
        :param min_degree_points: minimum number of points to complete the degree
        :param min_semester_points: minimum number of points in each semester
        :param max_semester_points: maximum number of points in each semester
        """
        self.__degree_courses = degree_courses
        self.__mandatory_points_left = mandatory_courses_points
        self.__total_points_left = min_degree_points
        self.__min_semester_points = min_semester_points
        self.__max_semester_points = max_semester_points
        self.__next_semester_num = 1
        self.__courses_so_far: set[int] = set()

    def add_semester(self, semester: Semester) -> "DegreePlan":
        """
        creates a new Degree Plan with the added semester
        :raises ValueError if the semester is invalid
        :param semester: a Semester object
        :return: the new Degree Plan with the added semester
        """
        if any(not self._is_valid_course(course) for course in semester.courses):
            raise ValueError("Semester is not allowed")

        new_degree_plan = self.__copy__()
        new_degree_plan.__next_semester_num += 1
        for course in semester.courses:
            new_degree_plan.__total_points_left -= course.points
            if course.is_mandatory:
                new_degree_plan.__mandatory_points_left -= course.points
            new_degree_plan.__courses_so_far.add(course.number)
        return new_degree_plan

    def _next_semester(self) -> str:
        return Semester.A if self.__next_semester_num % 2 == 1 else Semester.B

    def _is_valid_course(self, course: Course) -> bool:
        """
        checks if a course is invalid - means the course already placed in previous semester or there are
        prerequisites not satisfied or not in the right semester.
        :param course: a Course object
        :return: True iff the course is invalid
        """
        return (self._next_semester() == course.semester and
                course.number not in self.__courses_so_far and
                course.can_take_this_course(self.__courses_so_far))

    def get_legal_semesters(self) -> list[Semester]:
        """
        :return: list of all possible legal semesters according to the constraints.
        """
        legal_courses = filter(self._is_valid_course, self.__degree_courses)
        legal_course_subsets = chain.from_iterable(
            combinations(legal_courses, r) for r in range(len(legal_courses) + 1))
        legal_course_subsets = filter(
            lambda subset: self.__min_semester_points <= sum(course.points for course in subset) <=
                           self.__max_semester_points, legal_course_subsets)
        return [Semester(frozenset(subset)) for subset in legal_course_subsets]

    def is_legal_degree_plan(self) -> bool:
        """
        :return: True iff the plan meets all the requirements of the degree.
        """
        return self.__mandatory_points_left <= 0 and self.__total_points_left <= 0

    # __eq__ and __hash__ functions are needed for graph search when using 'visited' set.
    def __eq__(self, other) -> bool:
        if not isinstance(other, DegreePlan):
            return False
        return (
                self.__mandatory_points_left == other.__mandatory_points_left and
                self.__total_points_left == other.__total_points_left and
                self.__next_semester_num == other.__next_semester_num and
                self.__courses_so_far == other.__courses_so_far
        )

    def __hash__(self) -> int:
        return hash((
            self.__mandatory_points_left,
            self.__total_points_left,
            self.__next_semester_num,
            frozenset(self.__courses_so_far)
        ))

    def __copy__(self):
        new_plan = DegreePlan(self.__degree_courses, self.__mandatory_points_left, self.__total_points_left,
                              self.__min_semester_points, self.__max_semester_points)
        new_plan.__next_semester_num = self.__next_semester_num
        new_plan.__courses_so_far = self.__courses_so_far.copy()
        return new_plan
