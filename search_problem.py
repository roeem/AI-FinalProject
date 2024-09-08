import sys

from course import Course
from degree_plan import DegreePlan
from gui import run_gui
from input_loader import load_degree_plan
from local_degree_planning_problem import DegreePlanningProblem
from local_search import *


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


@timer
def main():
    algorithm = sys.argv[1]
    input_file_path = "input_files/" + sys.argv[2]
    min_semester_points = int(sys.argv[3])
    max_semester_points = int(sys.argv[4])

    mandatory_points, target_points, degree_courses = load_degree_plan(input_file_path)

    degree_planning_search_params = {
        'degree_courses': degree_courses,
        'mandatory_points': mandatory_points,
        'target_points': target_points,
        'min_semester_points': min_semester_points,
        'max_semester_points': max_semester_points
    }

    # print(f"Degree: {input_file_path[12:-5]}")
    # print("upper bound avg: ", get_upper_bound_avg(degree_courses, target_points))
    # exit(0)

    # if problem == 'min_time':
    #     degree_planning_search = DegreePlanningMinTime(**degree_planning_search_params)
    #     heuristic = degree_planning_problems.min_time_heuristic
    # elif problem == 'max_avg':
    #     degree_planning_search = DegreePlanningMaxAvg(**degree_planning_search_params)
    #     heuristic = degree_planning_problems.max_avg_heuristic
    dpp = DegreePlanningProblem(**degree_planning_search_params)

    if algorithm == 'hill':
        solution: DegreePlan = hill_climbing(dpp)
    elif algorithm == 'sa_exp':
        solution: DegreePlan = simulated_annealing(dpp, exp_cool_schedule)
    elif algorithm == 'sa_lin':
        solution: DegreePlan = simulated_annealing(dpp, linear_cool_schedule)
    elif algorithm == 'sa_log':
        solution: DegreePlan = simulated_annealing(dpp, log_cool_schedule)
    else:
        raise ValueError('Invalid algorithm type')

    dec = "###############################"
    print(f"{dec}DEGREE PLAN:{dec}")
    run_gui(solution)
    print(f"Expanded: {dpp.expanded}\n{solution}")


if __name__ == '__main__':
    main()
