from prerequisites import Prerequisites


class Course:
    """
    This class represent a Course of some degree.
    """

    def __init__(self, course_number: int, semester_type: str, name: str, points: int, avg_grade: float,
                 is_mandatory: bool = False, prerequisites: Prerequisites = None):
        """
        :param course_number: the number of the course
        :param semester_type: the semester in which the course is studied - should be 'A' or 'B'.
        :param name: the course name.
        :param prerequisites: prerequisites for this course.
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
        return self.__number

    @property
    def semester_type(self) -> str:
        return self.__semester_type

    @property
    def name(self) -> str:
        return self.__name

    @property
    def points(self) -> int:
        return self.__points

    @property
    def avg_grade(self) -> float:
        return self.__avg_grade

    @property
    def is_mandatory(self) -> bool:
        return self.__is_mandatory

    @property
    def prerequisites(self) -> Prerequisites:
        return self.__prerequisites

    def can_take_this_course(self, finished_courses: set[int]) -> bool:
        """
        Checks whether a student who studied all the courses in the set can take this course
        :param finished_courses: set of course numbers the student already done.
        :return: True if and only if the student can take this course.
        """
        return self.__prerequisites.meets_prerequisites(finished_courses)

    def __repr__(self) -> str:
        """
        For debugging
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
        if not isinstance(other, Course):
            return False
        return self.number == other.number and self.semester_type == other.semester_type

    def __hash__(self):
        return hash((self.number, self.semester_type))
