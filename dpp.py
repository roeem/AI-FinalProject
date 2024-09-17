import sys
from enum import Enum

from course import Course
from graph_search.degree_planning_problem import DegreePlanningProblem, max_avg_heuristic
from graph_search.search import bfs, dfs, ucs, astar
from local_search.local_degree_plan import LocalDegreePlan
from gui import run_gui
from input_loader import load_degree_plan
from local_search.local_degree_planning_problem import LocalDegreePlanningProblem
from local_search.local_search_ import *
import time


class DegreeLoad(Enum):
    LOW = 10, 20
    MEDIUM = 15, 25
    HIGH = 20, 30


def is_valid_degree_plan(degree_plan: LocalDegreePlan, degree_planning_params):
    # TODO REMOVE BEFORE SUBMISSION
    if degree_plan.total_points != degree_planning_params['target_points']:
        return False
    if degree_plan.mandatory_points != degree_planning_params['mandatory_points']:
        return False

    return True


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("Time: %s seconds" % (time.time() - start))
        return result

    return wrapper


def calculate_avg(courses: list[Course]) -> tuple[float, int]:
    points = 0
    grade_sum = 0
    for course in courses:
        points += course.points
        grade_sum += course.avg_grade * course.points
    return grade_sum / points, points


def num_of_semesters(courses: list[Course]) -> int:
    semester = "A"
    count = 0
    for course in courses:
        if course.semester_type != semester:
            count += 1
            semester = course.semester_type
    return count


def run_graph_search_main(algorithm: str, degree_planning_search_params: dict):
    degree_planning_search = DegreePlanningProblem(**degree_planning_search_params)

    if algorithm == 'bfs':
        solution = bfs(degree_planning_search)
    elif algorithm == 'dfs':
        solution = dfs(degree_planning_search)
    elif algorithm == 'astar':
        solution = astar(degree_planning_search, max_avg_heuristic)
    elif algorithm == 'ucs':
        solution = ucs(degree_planning_search)
    else:
        raise ValueError('Invalid algorithm type')

    if not solution:
        print("Sorry...\nThere is no solution for this input.")
        return
    # todo: fix gui class to handle both degree plans and use gui here.
    avg, points = calculate_avg(solution)
    print(f"num of courses: {len(solution)}")
    print(f"num of semesters: {num_of_semesters(solution)}")
    print(f"Target points: {degree_planning_search_params['target_points']}")
    print(f"Mandatory points: {degree_planning_search_params['mandatory_points']}")
    print(f"Average: {avg}")
    print(f"Points: {points}")
    print(f"Expanded: {degree_planning_search.expanded}")
    for course in solution:
        print(course)


def run_local_search_main(algorithm: str, degree_planning_search_params: dict):
    dpp = LocalDegreePlanningProblem(**degree_planning_search_params)

    if algorithm == 'hill':
        solution: LocalDegreePlan = hill_climbing(dpp)
    elif algorithm == 'sa_exp':
        solution: LocalDegreePlan = simulated_annealing(dpp, exp_cool_schedule)
    elif algorithm == 'sa_lin':
        solution: LocalDegreePlan = simulated_annealing(dpp, linear_cool_schedule)
    elif algorithm == 'sa_log':
        solution: LocalDegreePlan = simulated_annealing(dpp, log_cool_schedule)
    elif algorithm == 'beam':
        solution: LocalDegreePlan = stochastic_beam_search(dpp, k=50)
    else:
        raise ValueError('Invalid algorithm type')

    dec = "###############################"
    print(f"{dec}DEGREE PLAN:{dec}")
    # run_gui(solution)
    print(f"Expanded: {dpp.expanded}\n{solution}")


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

    # tests(degree_courses, mandatory_points, max_semester_points, min_semester_points, target_points)

    # run_search(algorithm, degree_planning_search_params)
    print(test_local(degree_planning_search_params, lambda x:simulated_annealing(x,exp_cool_schedule), 50))
    #test_sa_param(degree_planning_search_params)


# TODO REMOVE!!!!!!!!!!!
def tests(degree_courses, mandatory_points, max_semester_points, min_semester_points, target_points):
    ldpp = LocalDegreePlanningProblem(degree_courses, mandatory_points, target_points, min_semester_points,
                                      max_semester_points)
    states = []
    for _ in range(10):
        states.append(ldpp.get_initial_state())
    states.sort(key=lambda x: ldpp.fitness(x))
    for s in states:
        print(f"Fitness Score= {ldpp.fitness(s)}\n The Degree Plan:\n{s}\n")
        print("\n=============================================================\n")


def test_sa_param(degree_planning_search_params):
    epss, T0s, alphas = [1e-5, 1e-7, 1e-9, 1e-12, 1e-15, 1e-20], [100, 1000, 5000, 10000, 20000], \
        [0.7, 0.8, 0.9, 0.95, 0.99, 0.995, 0.999]
    for alpha in alphas:
        for eps in epss:
            for T0 in T0s:
                successes = 0
                avg = 0
                for i in range(10):
                    dpp = LocalDegreePlanningProblem(**degree_planning_search_params)
                    print(f"Started iteration {i}")
                    start_time = time.time()
                    solution: LocalDegreePlan = (
                        simulated_annealing(dpp, schedule=lambda t: exp_cool_schedule(t, T0, alpha), eps=eps))
                    total_time = time.time() - start_time
                    # print(f"Params: eps={eps}, T0={T0}, alpha={alpha}")
                    # print(f"Average Grade: {solution.avg_grade}")
                    # print(f"Total Points: {solution.total_points}")
                    # print(f"Mandatory Points: {solution.mandatory_points}")
                    # print(f"Expanded: {dpp.expanded}")
                    # print(f"Time: {total_time}")
                    # print("\n==============================================\n")
                    if is_valid_degree_plan(solution, degree_planning_search_params):
                        successes += 1
                        avg += solution.avg_grade
                avg = 0 if successes == 0 else avg / successes
                print(f"Solution succeeded {successes} time out of 10, with success's avg = {avg}\n")
                print(f"Params: eps={eps}, T0={T0}, alpha={alpha}")

def test_local(degree_planning_search_params, algorithm, number_of_runs):
    # TODO: remove before submission
    runs = []
    expanded = 0
    for i in range(number_of_runs):
        print(f"Iteration num {i}")
        dpp = LocalDegreePlanningProblem(**degree_planning_search_params)
        start_time = time.time()
        solution: LocalDegreePlan = algorithm(dpp)
        total_time = time.time() - start_time
        runs.append((solution, total_time))
        expanded += dpp.expanded

    avg_expanded = expanded / number_of_runs
    legal_runs_avg = [run[0].avg_grade for run in runs if
                      is_valid_degree_plan(run[0], degree_planning_search_params)]
    avg_avg_grade = sum(legal_runs_avg) / len(legal_runs_avg)
    legal_ratio = len(legal_runs_avg) / number_of_runs

    print(f"Average Average Grade: {avg_avg_grade}")
    print(f"Legal Ratio: {legal_ratio}")
    print(f"Average Expanded: {avg_expanded}")
    return avg_avg_grade, legal_ratio


if __name__ == '__main__':
    main()
