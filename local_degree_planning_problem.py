import random

from course import Course
from degree_plan import DegreePlan
from local_search import LocalSearchProblem


class DegreePlanningProblem(LocalSearchProblem):

    def __init__(self, degree_courses: list[Course], mandatory_points: int,
                 target_points: int, min_semester_points, max_semester_points):

        self.__degree_courses = degree_courses
        self.__target_points = target_points
        self.__mandatory_points = mandatory_points
        self.__min_semester_points = min_semester_points
        self.__max_semester_points = max_semester_points
        self.__upper_bound = None
        self.expanded = 0

    @property
    def target_points(self) -> int:
        return self.__target_points

    @property
    def mandatory_points(self) -> int:
        return self.__mandatory_points

    def get_initial_state(self) -> DegreePlan:
        init_state = DegreePlan(self.__degree_courses)
        random_num_of_points = random.randint(1, self.__target_points)
        max_iter = 10000
        courses = self.__degree_courses.copy()
        while max_iter > 0 and init_state.total_points < random_num_of_points:
            random_course: Course = random.choice(courses)
            possible_semesters = init_state.possible_semesters_to_course(random_course)
            if possible_semesters:
                random_semester = random.choice(possible_semesters)
                init_state = init_state.add_course(random_course, random_semester)
                courses.remove(random_course)

            max_iter -= 1
        # return self.__degree_plan
        return init_state

    def get_neighbors(self, state: DegreePlan) -> list[DegreePlan]:
        self.expanded += 1
        neighbors = self._single_step_neighbors(state)
        neighbors.extend(self._double_step_neighbors(state))
        # TODO: maybe expand such that there are no duplicates in neighbors (probability wise!)
        neighbors = list(set(neighbors))
        return neighbors

    def fitness(self, state: DegreePlan) -> float:
        # preq, num pts in semester, mando and elective, avg grade
        miss_preq = state.sum_missing_prerequisites()  # todo: maybe remove
        exceeded_points = state.sum_exceeded_points_in_semesters(self.__min_semester_points,
                                                                 self.__max_semester_points)
        mandatory_left = self.__mandatory_points - state.mandatory_points
        elective_left = (self.__target_points - self.__mandatory_points) - (
                state.total_points - state.mandatory_points)
        avg = state.avg_grade
        # return -miss_preq + avg
        return avg - 5 * (5 * mandatory_left + 2 * elective_left + exceeded_points)
        # return avg - (miss_preq + exceeded_points + mandatory_left + elective_left)

    def get_upper_bound(self) -> float:
        if self.__upper_bound:
            return self.__upper_bound
        mandatory_courses = {}
        for course in self.__degree_courses:
            if course.is_mandatory:
                if course.number in mandatory_courses:
                    max_option = max([mandatory_courses[course.number], course], key=lambda x: x.avg_grade)
                    mandatory_courses[course.number] = max_option
                else:
                    mandatory_courses[course.number] = course

        weighted_sum_mandatory = sum(
            [course.avg_grade * course.points for course in mandatory_courses.values()])
        sum_mandatory_points = sum([course.points for course in mandatory_courses.values()])
        # TODO: pass mandatory_points as a parameter and check legality

        elective_courses = {}
        for course in self.__degree_courses:
            if not course.is_mandatory:
                if course.number in elective_courses:
                    max_option = max([elective_courses[course.number], course], key=lambda x: x.avg_grade)
                    elective_courses[course.number] = max_option
                else:
                    elective_courses[course.number] = course

        # Sort elective courses by avg grade in descending order
        elective_courses = sorted(elective_courses.values(), key=lambda x: x.avg_grade)

        sum_elective_points, weighted_sum_elective = 0, 0
        elective_points_left = self.__target_points - sum_mandatory_points

        course = elective_courses[-1]
        while sum_elective_points + elective_courses[-1].points <= elective_points_left:
            course = elective_courses.pop()
            sum_elective_points += course.points
            weighted_sum_elective += course.avg_grade * course.points

        weighted_sum_elective += course.avg_grade * (elective_points_left - sum_elective_points)
        total_average = (weighted_sum_mandatory + weighted_sum_elective) / self.__target_points
        assert total_average <= 100
        self.__upper_bound = total_average
        return self.__upper_bound

    # region ########### HELPERS ###########

    def _single_step_neighbors(self, state: DegreePlan) -> list[DegreePlan]:
        neighbors = []
        removable_courses = state.possible_courses_to_remove()
        for c in self.__degree_courses:
            if c in removable_courses:
                neighbors.append(state.remove_course(c))
            elif not state.took_course_number(
                    c.number) and state.total_points + c.points <= self.__target_points:
                available_semesters = state.possible_semesters_to_course(c)
                neighbors.extend([state.add_course(c, sem) for sem in available_semesters])
        return neighbors

    def _double_step_neighbors(self, state: DegreePlan) -> list[DegreePlan]:
        neighbors = []
        removable_courses = state.possible_courses_to_remove()
        for c1 in removable_courses:
            for c2 in self.__degree_courses:
                if c1 == c2:
                    continue
                # TODO: check efficiency
                new_state: DegreePlan = state.remove_course(c1)
                if c2 in removable_courses:
                    new_state: DegreePlan = new_state.remove_course(c2)
                if new_state.took_course_number(c2.number):
                    continue

                if new_state.total_points + c2.points <= self.__target_points:
                    available_semesters = new_state.possible_semesters_to_course(c2)
                    neighbors.extend([new_state.add_course(c2, sem) for sem in available_semesters])
        return neighbors

    # endregion
