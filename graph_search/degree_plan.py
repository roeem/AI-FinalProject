from course import Course


class Semester:
    """
    Represents the types of semesters available.

    - A: Represents the first semester type.
    - B: Represents the second semester type.
    """
    A = "A"
    B = "B"


class DegreePlan:
    """
    Represents a Degree Plan for a student.

    This class is immutable and serves as the state in a search problem for degree planning.
    Each Degree Plan (state) contains information about the courses required to finish the degree,
    all courses already placed in previous semesters, and all courses available for the degree.
    """

    def __init__(self, degree_courses: list[Course]):
        """
        Initializes a Degree Plan with the provided list of available courses.

        :param degree_courses: A list of courses available for the degree.
        :type degree_courses: list[Course]
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
        Creates a new Degree Plan with the added course in the current semester.

        :raises ValueError: If the course cannot be added due to semester or other constraints.
        :param course: The course to be added to the degree plan.
        :type course: Course
        :param min_semester_points: Minimum points required for the current semester to be valid.
        :type min_semester_points: int
        :param max_semester_points: Maximum points allowed for the current semester.
        :type max_semester_points: int
        :return: A new Degree Plan instance with the course added.
        :rtype: DegreePlan
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

        new_degree_plan.__avg_grade = (
                (course.avg_grade * course.points + self.__avg_grade * self.__total_points) /
                new_degree_plan.__total_points)
        return new_degree_plan

    @property
    def mandatory_points(self) -> int:
        """
        Returns the total number of mandatory course points accumulated so far.

        :return: Total number of mandatory course points.
        :rtype: int
        """
        return self.__mandatory_points

    @property
    def total_points(self) -> int:
        """
        Returns the total number of points accumulated so far.

        :return: Total points accumulated.
        :rtype: int
        """
        return self.__total_points

    @property
    def current_semester_type(self) -> str:
        """
        Returns the current semester type ("A" or "B").

        :return: The current semester type.
        :rtype: str
        """
        return Semester.A if self.__current_semester_num % 2 == 1 else Semester.B

    @property
    def avg_grade(self) -> float:
        """
        Returns the current average grade based on the courses taken so far.

        :return: Average grade of courses taken.
        :rtype: float
        """
        return self.__avg_grade

    def is_valid_course(self, course: Course, min_semester_points: int, max_semester_points: int) -> bool:
        """
        Checks if the given course can be added to the current degree plan.

        A course is valid if:
        - It is offered in the current semester.
        - The prerequisites for the course are satisfied.
        - The total points for the semester stay within the allowed range.

        :param course: The course to be checked for validity.
        :type course: Course
        :param min_semester_points: Minimum points required for the current semester.
        :type min_semester_points: int
        :param max_semester_points: Maximum points allowed for the current semester.
        :type max_semester_points: int
        :return: True if the course is valid for the current semester; False otherwise.
        :rtype: bool
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
        Returns a list of all courses that can legally be taken in the current semester
        according to the constraints.

        :param min_semester_points: Minimum points required for the semester to be valid.
        :type min_semester_points: int
        :param max_semester_points: Maximum points allowed in the semester.
        :type max_semester_points: int
        :return: List of all valid courses for the current semester.
        :rtype: list[Course]
        """
        return [course for course in self.__degree_courses if
                self.is_valid_course(course, min_semester_points, max_semester_points)]

    def get_optional_courses(self) -> frozenset[Course]:
        """
        Returns a set of optional courses that have not been taken yet.

        :return: A set of courses that are optional.
        :rtype: frozenset[Course]
        """
        optional = {course for course in self.__degree_courses if
                    course.number not in self.__courses_so_far.keys()}
        return frozenset(optional)

    def __eq__(self, other) -> bool:
        """
        Checks if this Degree Plan is equal to another Degree Plan.

        Two Degree Plans are equal if they have the same courses and are in the same semester.

        :param other: The Degree Plan to compare with.
        :type other: DegreePlan
        :return: True if both Degree Plans are equal; False otherwise.
        :rtype: bool
        """
        if not isinstance(other, DegreePlan):
            return False
        return (
                self.current_semester_type == other.current_semester_type and
                {course for course, sem in self.__courses_so_far.values()} ==
                {course for course, sem in other.__courses_so_far.values()}
        )

    def __hash__(self) -> int:
        """
        Returns a hash value for this Degree Plan, enabling it to be used in hash-based collections
        such as sets and dictionaries.

        :return: Hash value for the Degree Plan.
        :rtype: int
        """
        return hash((frozenset({course for course, sem in self.__courses_so_far.values()}),
                     self.current_semester_type))

    def __copy__(self) -> "DegreePlan":
        """
        Creates a copy of the current Degree Plan.

        :return: A new Degree Plan that is a copy of the current one.
        :rtype: DegreePlan
        """
        new_plan = DegreePlan(self.__degree_courses)
        new_plan.__mandatory_points = self.__mandatory_points
        new_plan.__total_points = self.__total_points
        new_plan.__current_semester_num = self.__current_semester_num
        new_plan.__courses_so_far = self.__courses_so_far.copy()
        new_plan.__avg_grade = self.__avg_grade
        new_plan.__current_semester_points = self.__current_semester_points
        return new_plan
