import math

from course import Course
from search import SearchProblem
from degree_plan import DegreePlan, Semester


class DegreePlanningMinTime(SearchProblem):
    """
    Implementation of Search Problem for Degree Planning problem.
    """

    def __init__(self, degree_courses: frozenset[Course], mandatory_points: int,
                 target_points: int, min_semester_points: int = 0, max_semester_points: int = math.inf):
        self.degree_plan = DegreePlan(degree_courses)
        self.__target_points = target_points
        self.__mandatory_points = mandatory_points
        self.__min_semester_points = min_semester_points
        self.__max_semester_points = max_semester_points
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
        # TODO: check >=
        return (state.total_points >= self.__target_points and
                state.mandatory_points >= self.__mandatory_points)

    def get_successors(self, state: DegreePlan) -> list[tuple[DegreePlan, Semester, float]]:
        """
        :param state: a degree plan
        :return: for a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.add_semester(semester), semester, 1)
                for semester in
                state.get_legal_semesters(self.__min_semester_points, self.__max_semester_points)]

    def get_cost_of_actions(self, actions: list[Semester]) -> float:
        """
        :param actions: list of semesters
        :return: sum of all cost of each semester.
        """
        return len(actions)


class DegreePlanningMaxAvg(SearchProblem):
    """
    Implementation of Search Problem for Degree Planning problem.
    """

    def __init__(self, degree_courses: frozenset[Course], mandatory_points: int,
                 target_points: int, min_semester_points: int = 0, max_semester_points: int = math.inf):
        self.degree_plan = DegreePlan(degree_courses)
        self.__target_points = target_points
        self.__mandatory_points = mandatory_points
        self.__min_semester_points = min_semester_points
        self.__max_semester_points = max_semester_points
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
        return (state.total_points == self.__target_points and
                state.mandatory_points == self.__mandatory_points)

    def get_successors(self, state: DegreePlan) -> list[tuple[DegreePlan, Semester, float]]:
        """
        :param state: a degree plan
        :return: for a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.add_semester(semester), semester, self._get_cost_of_action(semester))
                for semester in
                state.get_legal_semesters(self.__min_semester_points, self.__max_semester_points)]

    def get_cost_of_actions(self, actions: list[Semester]) -> float:
        """
        :param actions: list of semesters
        :return: sum of all cost of each semester.
        """
        return sum(self._get_cost_of_action(action) for action in actions)

    def _get_cost_of_action(self, action: Semester) -> float:
        return (100 - action.avg_grade) * (action.points / self.__target_points)
