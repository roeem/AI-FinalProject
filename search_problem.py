import sys

import degree_planning_problems
from degree_planning_problems import *
from input_loader import load_degree_plan
from search import bfs, dfs, astar, ucs


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
    problem = sys.argv[1]
    algorithm = sys.argv[2]
    input_file_path = "input_files/" + sys.argv[3]
    min_semester_points = int(sys.argv[4])
    max_semester_points = int(sys.argv[5])

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

    if problem == 'min_time':
        degree_planning_search = DegreePlanningMinTime(**degree_planning_search_params)
        heuristic = degree_planning_problems.min_time_heuristic
    elif problem == 'max_avg':
        degree_planning_search = DegreePlanningMaxAvg(**degree_planning_search_params)
        heuristic = degree_planning_problems.max_avg_heuristic

    else:
        raise ValueError('Invalid problem type')

    if algorithm == 'bfs':
        solution = bfs(degree_planning_search)
    elif algorithm == 'dfs':
        solution = dfs(degree_planning_search)
    elif algorithm == 'astar':
        solution = astar(degree_planning_search, heuristic)
    elif algorithm == 'ucs':
        solution = ucs(degree_planning_search)
    else:
        raise ValueError('Invalid algorithm type')

    avg, points = calculate_avg(solution)
    print(f"num of courses: {len(solution)}")
    print(f"num of semesters: {num_of_semesters(solution)}")
    print(f"Target points: {target_points}")
    print(f"Mandatory points: {mandatory_points}")
    print(f"Average: {avg}, upperbound: {get_upper_bound_avg(degree_courses, target_points)}")
    print(f"Points: {points}")
    print(f"Expanded: {degree_planning_search.expanded}")
    for course in solution:
        print(course)


if __name__ == '__main__':
    main()
