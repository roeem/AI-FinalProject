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
        # TODO: add replace function - replace 2 courses in different semester or replace course in degree
        #  plan with course not in degree plan
        self.expanded += 1
        neighbors = []
        for c in self.__degree_courses:
            if state.took_course(c):
                neighbors.append(state.remove_course(c))

            elif not state.took_course_number(
                    c.number) and state.total_points + c.points <= self.__target_points:
                available_semesters = state.related_semesters_to_course(c)
                neighbors.extend([state.add_course(c, sem) for sem in available_semesters])

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
