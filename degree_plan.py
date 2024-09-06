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

    def __init__(self, degree_courses: list[Course]):
        """
        :param degree_courses: a frozenset of courses available for this degree
        """
        self.__degree_courses = degree_courses
        self.__mandatory_points = 0
        self.__total_points = 0
        self.__courses_so_far: dict[int, int] = {}
        self.__semesters: list[set[Course]] = []
        self.__avg_grade = 0

    def add_course(self, course: Course, semester: int) -> "DegreePlan":
        if len(self.__semesters) < semester or semester < 0 or course.number in self.__courses_so_far.keys():
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

    def remove_course(self, course: Course) -> "DegreePlan":
        if course.number not in self.__courses_so_far.keys():
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

    def took_course_number(self, course: int) -> bool:
        return course in self.__courses_so_far.keys()

    def took_course(self, course: Course) -> bool:
        return course.number in self.__courses_so_far.keys() and course in self.__semesters[
            self.__courses_so_far[course.number]]

    def related_semesters_to_course(self, course: Course) -> list[int]:
        course_semester = 0 if course.semester_type == "A" else 1
        return list(range(course_semester, len(self.__semesters) + 1, 2))

    def sum_missing_prerequisites(self) -> int:
        sum_miss_preq = 0
        taken_courses = set()
        for sem in self.__semesters:
            for c in sem:
                sum_miss_preq += c.get_num_miss_preqs(taken_courses)
            taken_courses |= sem  # Ron likes elegant ways to union sets
        return sum_miss_preq

    def sum_invalid_semesters(self, min_semester_points: int, max_semester_points: int) -> int:
        sem_points = map(lambda sem: sum(c.points for c in sem), self.__semesters)
        invalid_sem_error = 0
        for points in sem_points:
            if points < min_semester_points:
                invalid_sem_error += min_semester_points - points
            elif points > max_semester_points:
                invalid_sem_error += points - max_semester_points
        return invalid_sem_error

    @property
    def mandatory_points(self) -> int:
        return self.__mandatory_points

    @property
    def total_points(self) -> int:
        return self.__total_points

    @property
    def avg_grade(self) -> float:
        return self.__avg_grade

    # def get_legal_courses(self, min_semester_points: int, max_semester_points: int) -> list:
    #     """
    #     :return: list of all possible legal semesters according to the constraints.
    #     """
    #     return [course for course in self.__degree_courses if
    #             self.is_valid_course(course, min_semester_points, max_semester_points)]
    #
    # def get_optional_courses(self) -> frozenset[Course]:
    #     optional = {course for course in self.__degree_courses if
    #                 course.number not in self.__courses_so_far.keys()}
    #     return frozenset(optional)

    # __eq__ and __hash__ functions are needed for graph search when using 'visited' set.
    # def __eq__(self, other) -> bool:
    #     if not isinstance(other, DegreePlan):
    #         return False
    #     return True

    # def __hash__(self) -> int:
    #     return hash((frozenset({course for course, sem in self.__courses_so_far.values()}),
    #                  self.current_semester_type))

    def __copy__(self) -> "DegreePlan":
        new_plan = DegreePlan(self.__degree_courses)
        new_plan.__mandatory_points = self.__mandatory_points
        new_plan.__total_points = self.__total_points
        new_plan.__semesters = [semester.copy() for semester in self.__semesters]
        new_plan.__courses_so_far = self.__courses_so_far.copy()
        new_plan.__avg_grade = self.__avg_grade

        return new_plan

    def __str__(self):
        pts = "Total Points: " + str(self.__total_points) + "\n"
        m_pts = "Mandatory points: " + str(self.__mandatory_points) + "\n"
        avg = "Average grade: " + str(self.__avg_grade) + "\n"
        sems = "Semesters: " + str(len(self.__semesters)) + "\n"
        s = ""
        for i, sem in enumerate(self.__semesters):
            t = "A" if i % 2 == 0 else "B"
            s += f"Semester {t}\n"
            for course in sem:
                s += str(course) + "\n"
        return pts + m_pts + avg + sems + s
