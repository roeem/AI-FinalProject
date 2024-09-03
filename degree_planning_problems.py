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
        # if not successors:
        #     p = "No more courses!" if not courses else ""
        #     print(f"{p} Total Points are {state.total_points}, and mandatory : {state.mandatory_points}")
        return successors

    def get_cost_of_actions(self, actions: list[Course]) -> float:
        """
        :param actions: list of Courses
        :return: sum of all cost of each Course.
        """
        return sum(self._get_cost_of_action(action) for action in actions)

    def _get_cost_of_action(self, action: Course) -> float:
        cost = (100 - action.avg_grade) * (action.points / self.__target_points)
        return cost


def min_time_heuristic(state: DegreePlan, problem: DegreePlanningMinTime) -> float:
    avg_points_per_semester = (
            state.total_points / state.semester_count) if state.semester_count > 0 else problem.max_semester_points

    return (problem.target_points - state.total_points) / problem.max_semester_points


def get_upper_bound_avg(courses: frozenset[Course], total_points_left: int) -> float:
    if total_points_left == 0:
        return 100
    mandatory_courses = {}
    for course in courses:
        if course.is_mandatory:
            if course.number in mandatory_courses:
                max_option = max([mandatory_courses[course.number], course], key=lambda x: x.avg_grade)
                mandatory_courses[course.number] = max_option
            else:
                mandatory_courses[course.number] = course

    weighted_sum_mandatory = sum([course.avg_grade * course.points for course in mandatory_courses.values()])
    sum_mandatory_points = sum([course.points for course in mandatory_courses.values()])
    # TODO: pass mandatory_points as a parameter and check legality

    elective_courses = {}
    for course in courses:
        if not course.is_mandatory:
            if course.number in elective_courses:
                max_option = max([elective_courses[course.number], course], key=lambda x: x.avg_grade)
                elective_courses[course.number] = max_option
            else:
                elective_courses[course.number] = course

    # Sort elective courses by avg grade in descending order
    elective_courses = sorted(elective_courses.values(), key=lambda x: x.avg_grade)

    sum_elective_points, weighted_sum_elective = 0, 0
    elective_points_left = total_points_left - sum_mandatory_points

    while sum_elective_points + elective_courses[-1].points <= elective_points_left:
        course = elective_courses.pop()
        sum_elective_points += course.points
        weighted_sum_elective += course.avg_grade * course.points

    if sum_elective_points == 0:
        elective_avg = 100
    else:
        elective_avg = weighted_sum_elective / sum_elective_points
    # TODO: multiply last course instead of avg
    total_average = (weighted_sum_mandatory + elective_avg * elective_points_left) / total_points_left
    return total_average


def max_avg_heuristic(state: DegreePlan, problem: DegreePlanningMaxAvg) -> float:
    points_left = problem.target_points - state.total_points
    lef_avg = get_upper_bound_avg(state.get_optional_courses(), points_left)
    res = (100 - lef_avg) * points_left / problem.target_points  # TODO: why not deterministic and optimal 81.3, 81.15
    return res
