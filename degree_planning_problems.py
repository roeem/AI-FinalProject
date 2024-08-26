from search import SearchProblem
from degree_plan import DegreePlan


class DegreePlanningSearch(SearchProblem):
    def __init__(self):
        self.degree_plan = DegreePlan()
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
        pass  # TODO

    def get_successors(self, state: DegreePlan) -> list[tuple[DegreePlan, ..., float]]:
        """
        todo: * understand what should be an action (in blokus it was the object Move).
              * blokus doc and implementation below.
              * maybe a semester.
        :param state: a degree plan
        :return:
        """
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions) -> float:
        """
        todo: after understanding what is an action.
        :param actions:
        :return:
        """
        pass
