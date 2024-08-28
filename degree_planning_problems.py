import math

from course import Course
from search import SearchProblem
from degree_plan import DegreePlan, Semester


class DegreePlanningSearch(SearchProblem):
    """
    Implementation of Search Problem for Degree Planning problem.
    """

    def __init__(self, degree_courses: frozenset[Course], mandatory_courses_points: int,
                 min_degree_points: int, min_semester_points: int = 0, max_semester_points: int = math.inf):
        self.degree_plan = DegreePlan(degree_courses, mandatory_courses_points, min_degree_points,
                                      min_semester_points, max_semester_points)
        self.expanded = 0

    def get_start_state(self) -> DegreePlan:
        """
        :return: the start state for the search problem
        """
        return self.degree_plan

    def is_goal_state(self, state: DegreePlan) -> bool:
        """
        :param state: a degree plan
        :return: true if and only if the state is a valid goal state
        """
        return state.is_legal_degree_plan()

    def get_successors(self, state: DegreePlan) -> list[tuple[DegreePlan, Semester, float]]:
        """
        TODO: understand what should be the cost (now is 1) - if we will decide to handle avg grades
              the cost could be the loss in the final avg grade. For example: the degree total points is 134
              and the semester I took is 10 points with weighted avg of 85, so -
              the loss is (100-85)*(10/134).
              this way modeling in legal way but not good - because more courses == more losses (most of
              the times) so it will prefer less courses in semester (but maybe it will be good if we will
              limit the minimum points in each semester). Every other idea for costs that I could think of
              does not fit the problem of a star search.
        :param state: a degree plan
        :return: for a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.add_semester(semester), semester, 1) for semester in state.get_legal_semesters()]

    def get_cost_of_actions(self, actions) -> float:
        """
        todo: after understanding what should be the cost of an action.
        :param actions:
        :return:
        """
        pass
