from course import Course
from itertools import chain, combinations, tee


class Semester:
    """
    This class represent a Semester.
    """
    A = 'A'
    B = 'B'

    def __init__(self, courses: frozenset[Course], semester_type: str):
        self.__courses = courses
        self.__semester_type = semester_type
        self.__avg_grade = None
        self.__points = None

    @property
    def courses(self) -> frozenset[Course]:
        return self.__courses

    @property
    def semester_type(self) -> str:
        return self.__semester_type

    @property
    def avg_grade(self) -> float:
        if self.__avg_grade is not None:
            return self.__avg_grade
        self.__avg_grade, self.__points = self._calc_avg_grade_and_points()
        return self.__avg_grade

    @property
    def points(self) -> int:
        if self.__points is not None:
            return self.__points
        self.__avg_grade, self.__points = self._calc_avg_grade_and_points()
        return self.__points

    def _calc_avg_grade_and_points(self) -> tuple[float, int]:
        points = 0
        grade_sum = 0
        for course in self.courses:
            points += course.points
            grade_sum += course.avg_grade * course.points
        return grade_sum / points, points

    def __repr__(self) -> str:
        """
        For debugging
        """
        return (
                f"Semester {self.semester_type}:\n" +
                "\n".join([course.__repr__() for course in self.courses])
        )


class DegreePlan:
    """
    This class represent a Degree Plan.
    This class is immutable and can be used as state in search problem.
    Each Degree Plane (state) contains the requirements for finishing the degree, all courses already
    placed in previous semesters, all courses available fot this degree and more.
    """

    def __init__(self, degree_courses: frozenset[Course]):
        """
        :param degree_courses: a frozenset of courses available for this degree
        """
        self.__degree_courses = degree_courses
        self.__mandatory_points = 0
        self.__total_points = 0
        self.__next_semester_num = 1
        self.__courses_so_far: dict[int, Course] = {}

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
            new_degree_plan.__total_points += course.points
            if course.is_mandatory:
                new_degree_plan.__mandatory_points += course.points
            new_degree_plan.__courses_so_far[course.number] = course
        return new_degree_plan

    @property
    def mandatory_points(self) -> int:
        return self.__mandatory_points

    @property
    def total_points(self) -> int:
        return self.__total_points

    @property
    def _next_semester_type(self) -> str:
        return Semester.A if self.__next_semester_num % 2 == 1 else Semester.B

    def _is_valid_course(self, course: Course) -> bool:
        """
        checks if a course is invalid - means the course already placed in previous semester or there are
        prerequisites not satisfied or not in the right semester.
        :param course: a Course object
        :return: True iff the course is invalid
        """
        return (self._next_semester_type == course.semester_type and
                course.number not in self.__courses_so_far.keys() and
                course.can_take_this_course(set(self.__courses_so_far)))

    def get_legal_semesters(self, min_semester_points: int, max_semester_points: int) -> list:
        """
        :return: list of all possible legal semesters according to the constraints.
        """
        legal_courses = [course for course in self.__degree_courses if self._is_valid_course(course)]
        legal_semesters = []

        # Prune subsets early based on points
        for r in range(1, len(legal_courses) + 1):
            for subset in combinations(legal_courses, r):
                total_points = sum(course.points for course in subset)
                if min_semester_points <= total_points <= max_semester_points:
                    legal_semesters.append(Semester(frozenset(subset), self._next_semester_type))
        return legal_semesters

    # __eq__ and __hash__ functions are needed for graph search when using 'visited' set.
    def __eq__(self, other) -> bool:
        if not isinstance(other, DegreePlan):
            return False
        return (
                self.__mandatory_points == other.__mandatory_points and
                self.__total_points == other.__total_points and
                self.__next_semester_num == other.__next_semester_num and
                self.__courses_so_far == other.__courses_so_far
        )

    def __hash__(self) -> int:
        return hash((
            self.__mandatory_points,
            self.__total_points,
            self.__next_semester_num,
            frozenset(self.__courses_so_far)
        ))

    def __copy__(self) -> "DegreePlan":
        new_plan = DegreePlan(self.__degree_courses)
        new_plan.__mandatory_points = self.__mandatory_points
        new_plan.__total_points = self.__total_points
        new_plan.__next_semester_num = self.__next_semester_num
        new_plan.__courses_so_far = self.__courses_so_far.copy()
        return new_plan
