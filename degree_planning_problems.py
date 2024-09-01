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

    @property
    def target_points(self) -> int:
        return self.__target_points

    @property
    def mandatory_points(self) -> int:
        return self.__mandatory_points

    @property
    def min_semester_points(self) -> int:
        return self.__min_semester_points

    @property
    def max_semester_points(self) -> int:
        return self.__max_semester_points

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

    @property
    def target_points(self) -> int:
        return self.__target_points

    @property
    def mandatory_points(self) -> int:
        return self.__mandatory_points

    @property
    def max_semester_points(self) -> int:
        return self.__max_semester_points

    @property
    def min_semester_points(self) -> int:
        return self.__min_semester_points

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

    def get_successors(self, state: DegreePlan) -> list[tuple[DegreePlan, Course, float]]:
        """
        :param state: a degree plan
        :return: for a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        self.expanded = self.expanded + 1
        if self.expanded % 10000 == 0:
            print(f"Expanded: {self.expanded}")

        if self.target_points - state.total_points < self.mandatory_points - state.mandatory_points:
            return []

        successors = []
        courses = state.get_legal_courses(self.__min_semester_points, self.__max_semester_points)
        for course in courses:
            if state.total_points + course.points <= self.__target_points:
                successors.append((state.add_course(course, self.__min_semester_points, self.__max_semester_points),
                                   course, self._get_cost_of_action(course)))
        if not successors:
            p = "No more courses!" if not courses else ""
            print(f"{p} Total Points are {state.total_points}, and mandatory : {state.mandatory_points}")
        return successors

    def get_cost_of_actions(self, actions: list[Course]) -> float:
        """
        :param actions: list of Courses
        :return: sum of all cost of each Course.
        """
        return sum(self._get_cost_of_action(action) for action in actions)

    def _get_cost_of_action(self, action: Course) -> float:
        return (100 - action.avg_grade) * (action.points / self.__target_points)


def min_time_heuristic(state: DegreePlan, problem: DegreePlanningMinTime) -> float:
    avg_points_per_semester = (
            state.total_points / state.semester_count) if state.semester_count > 0 else problem.max_semester_points

    return (problem.target_points - state.total_points) / problem.max_semester_points


def max_avg_heuristic(state: DegreePlan, problem: DegreePlanningMaxAvg) -> float:
    pts_left = problem.target_points - state.total_points
    left_avg = sum((course.avg_grade for course in state.get_optional_courses())) / sum(
        (course.points for course in state.get_optional_courses()))
    return (100 - left_avg) * pts_left / problem.target_points

def max_avg_h_1_1(state: DegreePlan, problem: DegreePlanningMaxAvg) -> float:
    pts_left_to_do = problem.target_points - state.total_points
    optional_courses = state.get_optional_courses()
    # optional_courses = sorted(optional_courses, key=lambda x: x.avg_grade/x.points , reverse=True)
    sum_of_potential_grade, points = 0, 0
    max_course = max(optional_courses, key=lambda x: x.avg_grade)
    # for course in optional_courses:
    #     if pts_left_to_do > 0:
    #         if course.points <= pts_left_to_do:
    #             pts_left_to_do -= course.points
    # sum_of_potential_grade += course.avg_grade*course.points
    # points += course.points
    # else:
    #     break
    # avg_potential_grade = sum_of_potential_grade / points
    return (100 - max_course.avg_grade) * pts_left_to_do / problem.target_points + (
            problem.mandatory_points - state.mandatory_points) * 0.12
