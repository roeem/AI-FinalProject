import random

from course import Course
from local_search.local_degree_plan import LocalDegreePlan
from local_search.local_search_ import LocalSearchProblem


class LocalDegreePlanningProblem(LocalSearchProblem):

    def __init__(self, degree_courses: list[Course], mandatory_points: int,
                 target_points: int, min_semester_points, max_semester_points):

        self.__degree_courses = degree_courses
        self.__target_points = target_points
        self.__mandatory_points = mandatory_points
        self.__elective_points = target_points - mandatory_points
        self.__min_semester_points = min_semester_points
        self.__max_semester_points = max_semester_points
        self.__max_semester_num = target_points // min_semester_points
        self.expanded = 0
        self.__MINIMUM_INIT_POINTS = self.__target_points // 3

    @property
    def target_points(self) -> int:
        return self.__target_points

    @property
    def mandatory_points(self) -> int:
        return self.__mandatory_points

    def get_initial_state(self) -> LocalDegreePlan:
        init_state = LocalDegreePlan()
        random_num_of_points = random.randint(0, self.__target_points)
        max_iter = 10000
        courses = self.__degree_courses.copy()
        while max_iter > 0 and init_state.total_points < random_num_of_points:
            random_course: Course = random.choice(courses)
            if (init_state.total_points - init_state.mandatory_points) + random_course.points * (
                    not random_course.is_mandatory) <= self.__elective_points:
                possible_semesters = init_state.possible_semesters_to_course(random_course,
                                                                             self.__min_semester_points,
                                                                             self.__max_semester_points,
                                                                             self.__max_semester_num)
                if possible_semesters:
                    random_semester = random.choice(possible_semesters)
                    init_state = init_state.add_course(random_course, random_semester)
                    courses.remove(random_course)

            max_iter -= 1
        return init_state

    def get_neighbors(self, state: LocalDegreePlan) -> list[LocalDegreePlan]:
        self.expanded += 1
        neighbors = self._single_step_neighbors(state)
        neighbors.extend(self._double_step_neighbors(state))
        neighbors = list(set(neighbors))
        return neighbors

    def fitness(self, state: LocalDegreePlan) -> float:
        avg = (state.avg_grade * state.total_points) / self.__target_points
        avg += 100 if (state.total_points == self.__target_points and state.mandatory_points ==
                       self.mandatory_points) else 0
        return avg

    # region ########### HELPERS ###########

    def _single_step_neighbors(self, state: LocalDegreePlan) -> list[LocalDegreePlan]:
        neighbors = []
        removable_courses = state.possible_courses_to_remove()
        elective_pts = state.total_points - state.mandatory_points
        for c in self.__degree_courses:
            if c in removable_courses:
                neighbors.append(state.remove_course(c))
            elif (not state.took_course_number(c.number) and
                  elective_pts + c.points * (not c.is_mandatory) <= self.__elective_points):
                available_semesters = state.possible_semesters_to_course(c, self.__min_semester_points,
                                                                         self.__max_semester_points,
                                                                         self.__max_semester_num)
                neighbors.extend([state.add_course(c, sem) for sem in available_semesters])
        return neighbors

    def _double_step_neighbors(self, state: LocalDegreePlan) -> list[LocalDegreePlan]:
        neighbors = []
        removable_courses = state.possible_courses_to_remove()
        for c1 in removable_courses:
            for c2 in self.__degree_courses:
                new_state: LocalDegreePlan = state.remove_course(c1)
                if c2 in removable_courses and c1 != c2:
                    new_state: LocalDegreePlan = new_state.remove_course(c2)
                if new_state.took_course_number(c2.number):
                    continue
                if (new_state.total_points - new_state.mandatory_points) + c2.points * (
                        not c2.is_mandatory) <= self.__elective_points:
                    available_semesters = new_state.possible_semesters_to_course(
                        c2, self.__min_semester_points, self.__max_semester_points, self.__max_semester_num)
                    neighbors.extend([new_state.add_course(c2, sem) for sem in available_semesters])
        return neighbors

    # endregion
