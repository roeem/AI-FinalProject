import sys
from enum import Enum
from typing import Optional, Union
from course import Course
from graph_search.degree_planning_problem import DegreePlanningProblem, max_avg_heuristic
from graph_search.search import dfs, ucs, astar
from local_search.local_degree_plan import LocalDegreePlan, Semester
from gui import run_gui
from input_loader import load_degree_plan
from local_search.local_degree_planning_problem import LocalDegreePlanningProblem
from local_search.local_search_ import *
import time


class DegreeLoad(Enum):
    LOW = 10, 20
    MEDIUM = 15, 25
    HIGH = 20, 30


def show_results(solution: Union[LocalDegreePlan, Optional[list[Course]]], expanded: int) -> None:
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
    run_gui(solution)


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("Time: %s seconds" % (time.time() - start))
        return result

    return wrapper


def run_graph_search_main(algorithm: str, degree_planning_search_params: dict) -> (
        tuple)[Optional[list[Course]], int]:
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
    dpp = LocalDegreePlanningProblem(**degree_planning_search_params)
    if algorithm == 'hill':
        solution: LocalDegreePlan = hill(dpp)
    elif algorithm in ['sa', 'sa_exp']:
        solution: LocalDegreePlan = sa(dpp, exp_cool_schedule)
    elif algorithm == 'sa_lin':
        solution: LocalDegreePlan = sa(dpp, linear_cool_schedule)
    elif algorithm == 'sa_log':
        solution: LocalDegreePlan = sa(dpp, log_cool_schedule)
    elif algorithm == 'beam':
        solution: LocalDegreePlan = beam(dpp)
    else:
        raise ValueError('Invalid algorithm type')
    return solution, dpp.expanded


@timer
def main():
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
