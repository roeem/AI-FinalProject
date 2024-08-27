from prerequisites import Prerequisites


class Course:
    """
    This class represent a Course of some degree.
    """

    def __init__(self, course_number: int, semester_type: str, name: str, points: int,
                 is_mandatory: bool = False, prerequisites: Prerequisites = Prerequisites()):
        """
        :param course_number: the number of the course
        :param semester_type: the semester in which the course is studied - should be 'A' or 'B'.
        :param name: the course name.
        :param prerequisites: prerequisites for this course.
        """
        # TODO: in the future - maybe add course avg.
        self.__number: int = course_number
        self.__semester_type: str = semester_type
        self.__name: str = name
        self.__points: int = points
        self.__is_mandatory: bool = is_mandatory
        self.__prerequisites: Prerequisites = prerequisites

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
            f"Course(id={self.__number}, "
            f"name={self.__name}, "
            f"semester={self.__semester_type}, "
            f"prerequisites={self.__prerequisites.__repr__()}"
        )
