import sys

from course import Course
from graph_search.degree_planning_problem import DegreePlanningProblem, max_avg_heuristic
from graph_search.search import bfs, dfs, ucs, astar
from local_search.local_degree_plan import LocalDegreePlan
from gui import run_gui
from input_loader import load_degree_plan
from local_search.local_degree_planning_problem import LocalDegreePlanningProblem
from local_search.local_search_ import *


def timer(func):
    def wrapper(*args, **kwargs):
        import time
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


def run_graph_search_main(algorithm: str, degree_courses: list[Course], mandatory_points: int,
                          target_points: int, min_semester_points: int, max_semester_points: int):
    degree_planning_search_params = {
        'degree_courses': degree_courses,
        'mandatory_points': mandatory_points,
        'target_points': target_points,
        'min_semester_points': min_semester_points,
        'max_semester_points': max_semester_points
    }

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

    # todo: fix gui class to handle both degree plans and use gui here.
    avg, points = calculate_avg(solution)
    print(f"num of courses: {len(solution)}")
    print(f"num of semesters: {num_of_semesters(solution)}")
    print(f"Target points: {target_points}")
    print(f"Mandatory points: {mandatory_points}")
    print(f"Average: {avg}")
    print(f"Points: {points}")
    print(f"Expanded: {degree_planning_search.expanded}")
    for course in solution:
        print(course)


def run_local_search_main(algorithm: str, degree_courses: list[Course], mandatory_points: int,
                          target_points: int, min_semester_points: int, max_semester_points: int):
    degree_planning_search_params = {
        'degree_courses': degree_courses,
        'mandatory_points': mandatory_points,
        'target_points': target_points,
        'min_semester_points': min_semester_points,
        'max_semester_points': max_semester_points
    }
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
    min_semester_points = int(sys.argv[3])
    max_semester_points = int(sys.argv[4])

    mandatory_points, target_points, degree_courses = load_degree_plan(input_file_path)

    if algorithm in ["dfs", "bfs", "ucs", "astar"]:
        run_search = run_graph_search_main
    else:
        run_search = run_local_search_main

    # tests(degree_courses, mandatory_points, max_semester_points, min_semester_points, target_points)

    run_search(algorithm, degree_courses, mandatory_points, target_points,
               min_semester_points, max_semester_points)

#TODO REMOVE!!!!!!!!!!!
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


if __name__ == '__main__':
    main()
