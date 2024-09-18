import math

from course import Course
from graph_search.degree_plan import DegreePlan
from graph_search.search import SearchProblem


class DegreePlanningProblem(SearchProblem):
    """
    Implementation of a Search Problem for the Degree Planning problem.

    This class models the problem of planning a degree by creating and manipulating a degree plan.
    """

    def __init__(self, degree_courses: list[Course], mandatory_points: int,
                 target_points: int, min_semester_points: int = 0, max_semester_points: int = math.inf):
        """
        Initializes the Degree Planning Problem with given parameters.

        :param degree_courses: List of courses available for the degree.
        :type degree_courses: list[Course]
        :param mandatory_points: Number of mandatory points required.
        :type mandatory_points: int
        :param target_points: Total points required to complete the degree.
        :type target_points: int
        :param min_semester_points: Minimum points required in each semester.
        :type min_semester_points: int
        :param max_semester_points: Maximum points allowed in each semester.
        :type max_semester_points: int
        """
        self.degree_plan = DegreePlan(degree_courses)
        self.__target_points = target_points
        self.__mandatory_points = mandatory_points
        self.__min_semester_points = min_semester_points
        self.__max_semester_points = max_semester_points
        self.expanded = 0

    @property
    def target_points(self) -> int:
        """
        Returns the target points for the degree.

        :return: Target points required to complete the degree.
        :rtype: int
        """
        return self.__target_points

    @property
    def mandatory_points(self) -> int:
        """
        Returns the number of mandatory points required.

        :return: Mandatory points required for the degree.
        :rtype: int
        """
        return self.__mandatory_points

    def get_start_state(self) -> DegreePlan:
        """
        Returns the start state for the search problem.

        :return: The initial Degree Plan state.
        :rtype: DegreePlan
        """
        return self.degree_plan

    def is_goal_state(self, state: DegreePlan) -> bool:
        """
        Checks if the given state is a valid goal state for the search problem.

        A state is considered a goal state if the total points and mandatory points match the target values.

        :param state: The Degree Plan to check.
        :type state: DegreePlan
        :return: True if the state is a goal state; False otherwise.
        :rtype: bool
        """
        return (state.total_points == self.__target_points and
                state.mandatory_points == self.__mandatory_points)

    def get_successors(self, state: DegreePlan) -> list[tuple[DegreePlan, Course, float]]:
        """
        Returns a list of successor states for the given state.

        For a given state, this method returns a list of tuples, where each tuple consists of:
        - `successor`: A successor Degree Plan state.
        - `action`: The course added to the state.
        - `stepCost`: The cost of transitioning to the successor state.

        :param state: The Degree Plan state to expand.
        :type state: DegreePlan
        :return: List of successor states.
        :rtype: list[tuple[DegreePlan, Course, float]]
        """
        self.expanded = self.expanded + 1
        if self.expanded % 50000 == 0:
            print(f"Expanded: {self.expanded}")

        successors = []
        courses = state.get_legal_courses(self.__min_semester_points, self.__max_semester_points)
        for course in courses:
            if state.total_points + course.points <= self.__target_points:
                new_state = state.add_course(course, self.__min_semester_points, self.__max_semester_points)
                if (self.target_points - new_state.total_points >=
                        self.mandatory_points - new_state.mandatory_points):
                    successors.append((new_state, course, self._get_cost_of_action(course)))
        return successors

    def _get_cost_of_action(self, action: Course) -> float:
        """
        Computes the cost of taking a particular action (adding a course).

        The cost is computed based on the average grade of the course and its points relative to the
        target points.

        :param action: The course being added.
        :type action: Course
        :return: The cost of taking the action.
        :rtype: float
        """
        cost = (100 - action.avg_grade) * (action.points / self.__target_points)
        return round(cost * 100000)


def get_upper_bound_avg(courses: frozenset[Course], total_points_left: int) -> float:
    """
    Estimates the upper bound average grade achievable given a set of courses and remaining points.

    The estimate is computed based on the highest possible average grade for both mandatory and elective
    courses.

    :param courses: Set of available courses.
    :type courses: frozenset[Course]
    :param total_points_left: Total points left to achieve the target.
    :type total_points_left: int
    :return: The upper bound average grade.
    :rtype: float
    """
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

    course = elective_courses[-1]
    while sum_elective_points + elective_courses[-1].points <= elective_points_left:
        course = elective_courses.pop()
        sum_elective_points += course.points
        weighted_sum_elective += course.avg_grade * course.points

    weighted_sum_elective += course.avg_grade * (elective_points_left - sum_elective_points)
    total_average = (weighted_sum_mandatory + weighted_sum_elective) / total_points_left
    assert total_average <= 100
    return total_average


def max_avg_heuristic(state: DegreePlan, problem: DegreePlanningProblem) -> float:
    """
    Heuristic function for estimating the maximum average grade achievable from a given state.

    This heuristic calculates the estimated maximum average grade by considering the courses left
    and the total points required to reach the goal.

    :param state: The current Degree Plan state.
    :type state: DegreePlan
    :param problem: The Degree Planning Problem instance.
    :type problem: DegreePlanningProblem
    :return: The heuristic estimate of the maximum average grade.
    :rtype: float
    """
    points_left = problem.target_points - state.total_points
    left_avg = get_upper_bound_avg(state.get_optional_courses(), points_left)
    res = (100 - left_avg) * points_left / problem.target_points
    assert res >= 0
    return round(res * 100000)
