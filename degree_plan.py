from enum import Enum

from course import Course


class Semester:
    A = "A"
    B = "B"


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
        self.__current_semester_num = 1
        self.__courses_so_far: dict[int, tuple[Course, int]] = {}
        self.__avg_grade = 0
        self.__current_semester_points = 0

    def add_course(self, course: Course, min_semester_points: int, max_semester_points: int) -> "DegreePlan":
        """
        creates a new Degree Plan with the added semester
        :raises ValueError if the semester is invalid
        :param course: a Course object
        :return: the new Degree Plan with the added semester
        """
        if not self.is_valid_course(course, min_semester_points, max_semester_points):
            raise ValueError("Semester is not allowed")

        new_degree_plan = self.__copy__()

        if new_degree_plan.current_semester_type != course.semester_type:
            new_degree_plan.__current_semester_num += 1
            new_degree_plan.__current_semester_points = 0

        if course.is_mandatory:
            new_degree_plan.__mandatory_points += course.points

        new_degree_plan.__total_points += course.points
        new_degree_plan.__courses_so_far[course.number] = course, self.__current_semester_num
        new_degree_plan.__current_semester_points += course.points

        new_degree_plan.__avg_grade = ((course.avg_grade * course.points + self.__avg_grade * self.__total_points) /
                                       new_degree_plan.__total_points)
        return new_degree_plan

    @property
    def semester_count(self):
        return self.__current_semester_num - 1

    @property
    def mandatory_points(self) -> int:
        return self.__mandatory_points

    @property
    def total_points(self) -> int:
        return self.__total_points

    @property
    def current_semester_type(self) -> str:
        return Semester.A if self.__current_semester_num % 2 == 1 else Semester.B

    @property
    def avg_grade(self) -> float:
        return self.__avg_grade

    def is_valid_course(self, course: Course, min_semester_points: int, max_semester_points: int) -> bool:
        """
        checks if a course is invalid - means the course already placed in previous semester or there are
        prerequisites not satisfied or not in the right semester.
        :param course: a Course object
        :return: True iff the course is invalid
        """
        if self.current_semester_type != course.semester_type:
            did_finish_current_semester = min_semester_points <= self.__current_semester_points
            if not did_finish_current_semester:
                return False
        else:
            if self.__current_semester_points + course.points > max_semester_points:
                return False

        return (course.number not in self.__courses_so_far.keys()
                and course.can_take_this_course(
                    {course_num for course_num, (_, sem) in self.__courses_so_far.items() if
                     sem < self.__current_semester_num}))

    def get_legal_courses(self, min_semester_points: int, max_semester_points: int) -> list:
        """
        :return: list of all possible legal semesters according to the constraints.
        """
        return [course for course in self.__degree_courses if
                self.is_valid_course(course, min_semester_points, max_semester_points)]

    def get_optional_courses(self) -> frozenset[Course]:
        optional = {course for course in self.__degree_courses if course.number not in self.__courses_so_far.keys()}
        return frozenset(optional)

    # __eq__ and __hash__ functions are needed for graph search when using 'visited' set.
    def __eq__(self, other) -> bool:
        if not isinstance(other, DegreePlan):
            return False
        return (
                self.current_semester_type == other.current_semester_type and
                self.__courses_so_far == other.__courses_so_far
        )

    def __hash__(self) -> int:
        return hash((self.current_semester_type, frozenset(self.__courses_so_far)))

    def __copy__(self) -> "DegreePlan":
        new_plan = DegreePlan(self.__degree_courses)
        new_plan.__mandatory_points = self.__mandatory_points
        new_plan.__total_points = self.__total_points
        new_plan.__current_semester_num = self.__current_semester_num
        new_plan.__courses_so_far = self.__courses_so_far.copy()
        new_plan.__avg_grade = self.__avg_grade
        new_plan.__current_semester_points = self.__current_semester_points
        return new_plan
