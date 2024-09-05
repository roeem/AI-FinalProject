import math
from course import Course
from degree_plan import DegreePlan
from local_search import LocalSearchProblem


class LegalDegreePlanningProblem(LocalSearchProblem):

    def __init__(self, degree_courses: list[Course], mandatory_points: int,
                 target_points: int, min_semester_points: int = 0, max_semester_points: int = math.inf):
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
        # TODO maybe another mutate function
        self.expanded += 1
        neighbors = []
        for c in self.__degree_courses:
            if state.took_course(c):
                neighbors.append(state.remove_course(c))  # TODO IMPLEMENT remove course
            else:
                neighbors.append(state.add_course(c))  # TODO IMPLEMENT add course again

        return neighbors

    def fitness(self, state) -> float:
        super().fitness(state)
