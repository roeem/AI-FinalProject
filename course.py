from prerequisites import Prerequisites


class Course:
    """
    Represents a course in a degree program.
    """

    def __init__(self, course_number: int, semester_type: str, name: str, points: int, avg_grade: float,
                 is_mandatory: bool = False, prerequisites: Prerequisites = None):
        """
        Initializes the Course with its number, semester, name, points, average grade, whether it's
        mandatory, and prerequisites.

        :param course_number: The course number.
        :param semester_type: The semester when the course is offered ('A' or 'B').
        :param name: The name of the course.
        :param points: The credit points of the course.
        :param avg_grade: The average grade of students in this course.
        :param is_mandatory: Whether the course is mandatory (default: False).
        :param prerequisites: Prerequisites required for the course (default: empty Prerequisites object).
        """
        self.__number: int = course_number
        self.__semester_type: str = semester_type
        self.__name: str = name
        self.__points: int = points
        self.__avg_grade = avg_grade
        self.__is_mandatory: bool = is_mandatory
        self.__prerequisites: Prerequisites = prerequisites if prerequisites is not None else Prerequisites()

    @property
    def number(self) -> int:
        """
        Returns the course number.

        :return: The course number.
        :rtype: int
        """
        return self.__number

    @property
    def semester_type(self) -> str:
        """
        Returns the semester type ('A' or 'B').

        :return: The semester type.
        :rtype: str
        """
        return self.__semester_type

    @property
    def name(self) -> str:
        """
        Returns the course name.

        :return: The course name.
        :rtype: str
        """
        return self.__name

    @property
    def points(self) -> int:
        """
        Returns the number of credit points for the course.

        :return: The credit points.
        :rtype: int
        """
        return self.__points

    @property
    def avg_grade(self) -> float:
        """
        Returns the average grade for the course.

        :return: The average grade.
        :rtype: float
        """
        return self.__avg_grade

    @property
    def is_mandatory(self) -> bool:
        """
        Returns whether the course is mandatory.

        :return: True if the course is mandatory, False otherwise.
        :rtype: bool
        """
        return self.__is_mandatory

    @property
    def prerequisites(self) -> Prerequisites:
        """
        Returns the prerequisites for the course.

        :return: The prerequisites.
        :rtype: Prerequisites
        """
        return self.__prerequisites

    def can_take_this_course(self, finished_courses: set[int]) -> bool:
        """
        Checks if a student can take this course based on completed courses.

        :param finished_courses: A set of course numbers the student has completed.
        :return: True if the student meets the prerequisites, False otherwise.
        :rtype: bool
        """
        return self.__prerequisites.meets_prerequisites(finished_courses)

    def __repr__(self) -> str:
        """
        Returns a string representation of the course.

        :return: The string representation of the course.
        :rtype: str
        """
        return (
            f"Course(num={self.number}, "
            f"semester={self.semester_type}, "
            f'name="{self.name}", '
            f"points={self.points}, "
            f"avg_grade={self.avg_grade}, "
            f"is_mandatory={self.is_mandatory}, "
            f"prerequisites={self.prerequisites.__repr__()})"
        )

    def __eq__(self, other):
        """
        Compares this course with another course for equality.

        :param other: The course to compare with.
        :return: True if both courses have the same number and semester type, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Course):
            return False
        return self.number == other.number and self.semester_type == other.semester_type

    def __hash__(self):
        """
        Returns a hash value for the course based on its number and semester type.

        :return: The hash value.
        :rtype: int
        """
        return hash((self.number, self.semester_type))
