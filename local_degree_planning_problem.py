import math
from course import Course
from degree_plan import DegreePlan
from local_search import LocalSearchProblem


class DegreePlanningProblem(LocalSearchProblem):

    def __init__(self, degree_courses: list[Course], mandatory_points: int,
                 target_points: int, min_semester_points, max_semester_points):
        self.__degree_plan = DegreePlan(degree_courses)
        self.__degree_courses = degree_courses
        self.__target_points = target_points
        self.__mandatory_points = mandatory_points
        self.__min_semester_points = min_semester_points
        self.__max_semester_points = max_semester_points
        self.expanded = 0

    def get_initial_state(self) -> DegreePlan:
        return self.__degree_plan  # TODO make it random / not stupid

    def get_neighbors(self, state: DegreePlan) -> list[DegreePlan]:
        self.expanded += 1
        neighbors = self._single_step_neighbors(state)
        neighbors.extend(self._double_step_neighbors(state))

        return neighbors

    def fitness(self, state: DegreePlan) -> float:
        # preq, num pts in semester, mando and elective, avg grade
        miss_preq = state.sum_missing_prerequisites()
        invalid_sem = state.sum_invalid_semesters(self.__min_semester_points, self.__max_semester_points)
        mandatory_left = self.__mandatory_points - state.mandatory_points
        elective_left = self.__target_points - state.total_points
        avg = state.avg_grade
        # return -miss_preq + avg
        return avg - (miss_preq + invalid_sem + mandatory_left + elective_left)

    # region ########### HELPERS ###########

    def _single_step_neighbors(self, state:DegreePlan) -> list[DegreePlan]:
        neighbors = []
        for c in self.__degree_courses:
            if state.took_course(c):
                # Remove course taken
                neighbors.append(state.remove_course(c))
                # Add not taken course in all possible semesters
            elif not state.took_course_number(
                    c.number) and state.total_points + c.points <= self.__target_points:
                available_semesters = state.related_semesters_to_course(c)
                neighbors.extend([state.add_course(c, sem) for sem in available_semesters])
        return neighbors

    def _double_step_neighbors(self, state:DegreePlan) -> list[DegreePlan]:
        neighbors = []
        for c1 in self.__degree_courses:
            for c2 in self.__degree_courses:
                if state.took_course(c1):
                    # Remove course taken
                    new_state: DegreePlan = state.remove_course(c1)
                    if new_state.took_course(c2):
                        new_state: DegreePlan = new_state.remove_course(c2)
                    if new_state.took_course_number(c2.number):
                        continue

                    if new_state.total_points + c2.points <= self.__target_points:
                        available_semesters = new_state.related_semesters_to_course(c2)
                        neighbors.extend([new_state.add_course(c2, sem) for sem in available_semesters])
        return neighbors

# endregion
