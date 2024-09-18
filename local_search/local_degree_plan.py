from functools import reduce

from course import Course


class Semester:
    """
    Represents the types of semesters available.

    - A: Represents the first semester type.
    - B: Represents the second semester type.
    """
    A = "A"
    B = "B"


class LocalDegreePlan:
    """
    Represents a Degree Plan for a student.

    This class is immutable and can be used as a state in a search problem. It tracks the courses taken,
    mandatory and total points, and maintains a record of which courses are in which semesters.
    """

    def __init__(self):
        """
        Initializes a new LocalDegreePlan instance with zero mandatory points, total points,
        and an empty list of semesters.
        """
        self.__mandatory_points = 0
        self.__total_points = 0
        self.__courses_so_far: dict[int, int] = {}
        self.__semesters: list[set[Course]] = []
        self.__avg_grade = 0

    def add_course(self, course: Course, semester: int) -> "LocalDegreePlan":
        """
        Adds a course to a specified semester.

        :param course: The course to be added.
        :type course: Course
        :param semester: The semester index where the course will be added.
        :type semester: int
        :return: A new LocalDegreePlan instance with the course added.
        :rtype: LocalDegreePlan
        :raises ValueError: If the semester is invalid, the course is already taken, or the course semester
                            type does not match the semester.
        """
        semester_type = Semester.A if semester % 2 == 0 else Semester.B
        if (len(self.__semesters) < semester or semester < 0 or self.took_course_number(course.number) or
                semester_type != course.semester_type):
            raise ValueError("Invalid semester number/ course already taken.")

        new_degree_plan = self.__copy__()
        if len(self.__semesters) == semester:
            new_degree_plan.__semesters.append(set())

        if course.is_mandatory:
            new_degree_plan.__mandatory_points += course.points

        new_degree_plan.__total_points += course.points
        new_degree_plan.__courses_so_far[course.number] = semester
        new_degree_plan.__semesters[semester].add(course)
        new_degree_plan.__avg_grade = (
                (course.avg_grade * course.points + self.__avg_grade * self.__total_points) /
                new_degree_plan.__total_points)
        return new_degree_plan

    def remove_course(self, course: Course) -> "LocalDegreePlan":
        """
        Removes a course from the degree plan.

        :param course: The course to be removed.
        :type course: Course
        :return: A new LocalDegreePlan instance with the course removed.
        :rtype: LocalDegreePlan
        :raises ValueError: If the course has not been taken yet.
        """
        if not self.took_course(course):
            raise ValueError("Course not taken yet.")

        new_degree_plan = self.__copy__()

        if course.is_mandatory:
            new_degree_plan.__mandatory_points -= course.points

        new_degree_plan.__total_points -= course.points
        semester = new_degree_plan.__courses_so_far.pop(course.number)
        new_degree_plan.__semesters[semester].remove(course)
        if new_degree_plan.__total_points == 0:
            new_degree_plan.__avg_grade = 0
        else:
            new_degree_plan.__avg_grade = (
                    (self.__avg_grade * self.__total_points - course.avg_grade * course.points) /
                    new_degree_plan.__total_points)
        if semester == len(new_degree_plan.__semesters) - 1 and not new_degree_plan.__semesters[semester]:
            new_degree_plan.__semesters.pop()
        return new_degree_plan

    def took_course_number(self, course_number: int) -> bool:
        """
        Checks if a course with a given number has been taken.

        :param course_number: The course number to check.
        :type course_number: int
        :return: True if the course number has been taken, False otherwise.
        :rtype: bool
        """
        return course_number in self.__courses_so_far.keys()

    def took_course(self, course: Course) -> bool:
        """
        Checks if a specific course has been taken.

        :param course: The course to check.
        :type course: Course
        :return: True if the course has been taken, False otherwise.
        :rtype: bool
        """
        return course.number in self.__courses_so_far.keys() and course in self.__semesters[
            self.__courses_so_far[course.number]]

    def possible_semesters_to_course(self, course: Course, min_semester_points: int, max_semester_points: int,
                                     max_sem_num: int) -> list[int]:
        """
        Determines the possible semesters where a course can be added.

        :param course: The course to be added.
        :type course: Course
        :param min_semester_points: Minimum points required in a semester to open a new semester.
        :type min_semester_points: int
        :param max_semester_points: Maximum points allowed in a semester.
        :type max_semester_points: int
        :param max_sem_num: Maximum number of semesters allowed.
        :type max_sem_num: int
        :return: List of possible semester indices where the course can be added.
        :rtype: list[int]
        """
        if self.took_course_number(course.number):
            return []

        course_semester = 0 if course.semester_type == Semester.A else 1
        taken_courses: set[int] = set()
        possible_semesters = []

        for i in range(len(self.__semesters)):
            if i % 2 == course_semester and course.can_take_this_course(taken_courses):
                sum_points_in_sem = sum(c.points for c in self.__semesters[i])
                if sum_points_in_sem + course.points <= max_semester_points:
                    possible_semesters.append(i)
            taken_courses |= {c.number for c in self.__semesters[i]}

        # check if opening a new semester is possible
        if (len(self.__semesters) % 2 == course_semester and course.can_take_this_course(taken_courses) and
                len(self.__semesters) < max_sem_num):
            if len(self.__semesters) < 2 or sum(
                    c.points for c in self.__semesters[-2]) >= min_semester_points:
                possible_semesters.append(len(self.__semesters))

        return possible_semesters

    def possible_courses_to_remove(self) -> list[Course]:
        """
        Lists all courses that can be removed from the degree plan.

        :return: List of courses that can be removed.
        :rtype: list[Course]
        """
        possible_removals = []
        for sem in self.__semesters:
            for course in sem:
                if self.can_remove_course(course):
                    possible_removals.append(course)
        return possible_removals

    def can_remove_course(self, course_to_remove) -> bool:
        """
        Determines if a specific course can be removed from the degree plan.

        :param course_to_remove: The course to check for removal.
        :type course_to_remove: Course
        :return: True if the course can be removed, False otherwise.
        :rtype: bool
        """
        next_sem = self.__courses_so_far[course_to_remove.number] + 1
        taken_courses_nums = reduce(lambda acc, i: acc | {c.number for c in self.__semesters[i]},
                                    range(next_sem), set())
        taken_courses_nums -= {course_to_remove.number}
        for j in range(next_sem, len(self.__semesters)):
            for course in self.__semesters[j]:
                if not course.can_take_this_course(taken_courses_nums):
                    return False

        return True

    @property
    def mandatory_points(self) -> int:
        """
        Returns the total mandatory points accumulated.

        :return: The total mandatory points.
        :rtype: int
        """
        return self.__mandatory_points

    @property
    def total_points(self) -> int:
        """
        Returns the total points accumulated.

        :return: The total points.
        :rtype: int
        """
        return self.__total_points

    @property
    def avg_grade(self) -> float:
        """
        Returns the average grade across all courses.

        :return: The average grade.
        :rtype: float
        """
        return self.__avg_grade

    def __copy__(self) -> "LocalDegreePlan":
        """
        Creates a copy of the current LocalDegreePlan instance.

        :return: A new LocalDegreePlan instance that is a copy of the current instance.
        :rtype: LocalDegreePlan
        """
        new_plan = LocalDegreePlan()
        new_plan.__mandatory_points = self.__mandatory_points
        new_plan.__total_points = self.__total_points
        new_plan.__semesters = [semester.copy() for semester in self.__semesters]
        new_plan.__courses_so_far = self.__courses_so_far.copy()
        new_plan.__avg_grade = self.__avg_grade

        return new_plan

    def __str__(self):
        """
        Returns a string representation of the LocalDegreePlan instance.

        :return: A string representation of the degree plan.
        :rtype: str
        """
        pts = "Total Points: " + str(self.__total_points) + "\n"
        m_pts = "Mandatory points: " + str(self.__mandatory_points) + "\n"
        avg = "Average grade: " + str(self.__avg_grade) + "\n"
        sems = "Semesters: " + str(len(self.__semesters)) + "\n"
        s = ""
        for i, sem in enumerate(self.__semesters):
            t = "A" if i % 2 == 0 else "B"
            t += f" ({sum(c.points for c in sem)} points)"
            s += f"----------\n"
            s += f"Semester {t}\n"
            s += f"----------\n"
            for course in sorted(sem, key=lambda c: c.number):
                s += str(course) + "\n"
        return pts + m_pts + avg + sems + s

    def __eq__(self, other):
        """
        Checks if two LocalDegreePlan instances are equal.

        :param other: The other LocalDegreePlan instance to compare.
        :type other: LocalDegreePlan
        :return: True if the instances are equal, False otherwise.
        :rtype: bool
        """
        return str(self) == str(other)

    def __hash__(self):
        """
        Returns a hash of the LocalDegreePlan instance.

        :return: The hash of the instance.
        :rtype: int
        """
        return hash(str(self))
