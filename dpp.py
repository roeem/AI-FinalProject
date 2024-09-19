import sys
from enum import Enum
from typing import Optional, Union
from course import Course
from graph_search.degree_planning_problem import DegreePlanningProblem, max_avg_heuristic
from graph_search.search import dfs, ucs, astar
from local_search.local_degree_plan import LocalDegreePlan, Semester
from html_generator import generate_html
from input_loader import load_degree_plan
from local_search.local_degree_planning_problem import LocalDegreePlanningProblem
from local_search.local_search_ import *
import time


class DegreeLoad(Enum):
    """
    Enum representing degree load categories, specifying the minimum and maximum points
    a student can take per semester.
    """
    LOW = 10, 20
    MEDIUM = 15, 25
    HIGH = 20, 30


def show_results(solution: Union[LocalDegreePlan, Optional[list[Course]]], expanded: int) -> None:
    """
    Displays the solution for the degree plan and runs a GUI to visualize it.

    :param solution: The solution for the degree plan, either as a `LocalDegreePlan` or a list of `Course`
    objects.
    :type solution: Union[LocalDegreePlan, Optional[list[Course]]]
    :param expanded: The number of nodes expanded during the search process.
    :type expanded: int
    """
    if not solution:
        print("Sorry...\nThere is no solution for this input.")
        return
    if type(solution) is list:
        sol = solution
        solution = LocalDegreePlan()
        sem_num = 0
        for c in sol:
            if (c.semester_type == Semester.A and sem_num % 2 == 1 or c.semester_type == Semester.B and
                    sem_num % 2 == 0):
                sem_num += 1
            solution = solution.add_course(c, sem_num)

    dec = "###############################"
    print(f"{dec}DEGREE PLAN:{dec}")
    print(f"Expanded: {expanded}\n{solution}")
    generate_html(solution)


def timer(func):
    """
    Decorator function to time the execution of the decorated function.

    :param func: The function to be timed.
    :type func: callable
    :return: Wrapper function that prints the time taken to execute the function.
    :rtype: callable
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("Time: %s seconds" % (time.time() - start))
        return result

    return wrapper


def run_graph_search_main(algorithm: str, degree_planning_search_params: dict) -> (
        tuple)[Optional[list[Course]], int]:
    """
    Runs a graph search algorithm to solve the degree planning problem.

    :param algorithm: The search algorithm to be used ('dfs', 'ucs', 'astar').
    :type algorithm: str
    :param degree_planning_search_params: A dictionary of parameters required for the degree planning problem.
    :type degree_planning_search_params: dict
    :return: A tuple containing the solution (list of `Course` objects) and the number of expanded nodes.
    :rtype: tuple[Optional[list[Course]], int]
    """
    dpp = DegreePlanningProblem(**degree_planning_search_params)

    if algorithm == 'dfs':
        solution = dfs(dpp)
    elif algorithm == 'astar':
        solution = astar(dpp, max_avg_heuristic)
    elif algorithm == 'ucs':
        solution = ucs(dpp)
    else:
        raise ValueError('Invalid algorithm type')
    return solution, dpp.expanded


def run_local_search_main(algorithm: str, degree_planning_search_params: dict) -> tuple[LocalDegreePlan, int]:
    """
    Runs a local search algorithm to solve the degree planning problem.

    :param algorithm: The local search algorithm to be used ('hill', 'sa', 'beam', etc.).
    :type algorithm: str
    :param degree_planning_search_params: A dictionary of parameters required for the degree planning problem.
    :type degree_planning_search_params: dict
    :return: A tuple containing the solution (`LocalDegreePlan`) and the number of expanded nodes.
    :rtype: tuple[LocalDegreePlan, int]
    """
    dpp = LocalDegreePlanningProblem(**degree_planning_search_params)
    if algorithm == 'hill':
        solution: LocalDegreePlan = hill(dpp)
    elif algorithm == 'sa':
        solution: LocalDegreePlan = sa(dpp, exp_cool_schedule)
    elif algorithm == 'beam':
        solution: LocalDegreePlan = beam(dpp)
    else:
        raise ValueError('Invalid algorithm type')
    return solution, dpp.expanded


@timer
def main():
    """
    The main entry point of the program. Loads the input degree plan, determines the algorithm,
    and runs the appropriate search method (graph search or local search) to generate the degree plan.

    :raises ValueError: If the algorithm specified is not valid.
    """
    algorithm = sys.argv[1]
    input_file_path = "input_files/" + sys.argv[2]
    min_semester_points, max_semester_points = DegreeLoad[(sys.argv[3]).upper()].value

    mandatory_points, target_points, degree_courses = load_degree_plan(input_file_path)

    degree_planning_search_params = {
        'degree_courses': degree_courses,
        'mandatory_points': mandatory_points,
        'target_points': target_points,
        'min_semester_points': min_semester_points,
        'max_semester_points': max_semester_points
    }

    if algorithm in ["dfs", "bfs", "ucs", "astar"]:
        run_search = run_graph_search_main
    else:
        run_search = run_local_search_main

    solution, expanded = run_search(algorithm, degree_planning_search_params)
    show_results(solution, expanded)


if __name__ == '__main__':
    main()
