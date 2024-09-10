from functools import reduce

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

    def __init__(self):
        self.__mandatory_points = 0
        self.__total_points = 0
        self.__courses_so_far: dict[int, int] = {}
        self.__semesters: list[set[Course]] = []
        self.__avg_grade = 0

    def add_course(self, course: Course, semester: int) -> "DegreePlan":
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

    def remove_course(self, course: Course) -> "DegreePlan":
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

    def calc_avg(self) -> float:
        wsum, points = 0, 0
        for sem in self.__semesters:
            for c in sem:
                wsum += c.avg_grade * c.points
                points += c.points
        return 0 if points == 0 else wsum / points

    def took_course_number(self, course_number: int) -> bool:
        return course_number in self.__courses_so_far.keys()

    def took_course(self, course: Course) -> bool:
        return course.number in self.__courses_so_far.keys() and course in self.__semesters[
            self.__courses_so_far[course.number]]

    def possible_semesters_to_course(self, course: Course, max_semester_points: int) -> list[int]:
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
        if len(self.__semesters) % 2 == course_semester and course.can_take_this_course(taken_courses):
            possible_semesters.append(len(self.__semesters))

        return possible_semesters

    def possible_courses_to_remove(self) -> list[Course]:
        possible_removals = []
        for sem in self.__semesters:
            for course in sem:
                if self.can_remove_course(course):
                    possible_removals.append(course)
        return possible_removals

    def can_remove_course(self, course_to_remove) -> bool:
        next_sem = self.__courses_so_far[course_to_remove.number] + 1
        # TODO SLAP ROEE
        taken_courses_nums = set()
        for i in range(next_sem):
            taken_courses_nums |= {c.number for c in self.__semesters[i]}
        taken_courses2 = reduce(lambda acc, i: acc | {c.number for c in self.__semesters[i]}, range(next_sem),
                                set())
        assert taken_courses_nums == taken_courses2
        taken_courses_nums -= {course_to_remove.number}
        for i in range(next_sem, len(self.__semesters)):
            for course in self.__semesters[i]:
                if not course.can_take_this_course(taken_courses_nums):
                    return False

        return True

    def sum_missing_prerequisites(self) -> int:
        sum_miss_preq = 0
        taken_courses: set[int] = set()
        for sem in self.__semesters:
            for c in sem:
                sum_miss_preq += c.get_num_miss_preqs(taken_courses)
            taken_courses |= {course.number for course in sem}  # Ron likes elegant ways to union sets
        return sum_miss_preq

    def sum_exceeded_points_in_semesters(self, min_semester_points: int, max_semester_points: int) -> int:
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

    def __copy__(self) -> "DegreePlan":
        new_plan = DegreePlan()
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
            t += f" ({sum(c.points for c in sem)} points)"
            s += f"----------\n"
            s += f"Semester {t}\n"
            s += f"----------\n"
            for course in sorted(sem, key=lambda c: c.number):
                s += str(course) + "\n"
        return pts + m_pts + avg + sems + s

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))
