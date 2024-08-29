import sys
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


def calculate_avg(semesters: list[Semester]) -> tuple[float, int]:
    points = 0
    grade_sum = 0
    for semester in semesters:
        points += semester.points
        grade_sum += semester.avg_grade * semester.points
    return grade_sum / points, points


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

    if problem == 'min_time':
        degree_planning_search = DegreePlanningMinTime(**degree_planning_search_params)
    elif problem == 'max_avg':
        degree_planning_search = DegreePlanningMaxAvg(**degree_planning_search_params)
    else:
        raise ValueError('Invalid problem type')

    if algorithm == 'bfs':
        solution = bfs(degree_planning_search)
    elif algorithm == 'dfs':
        solution = dfs(degree_planning_search)
    elif algorithm == 'astar':
        solution = astar(degree_planning_search)
    elif algorithm == 'ucs':
        solution = ucs(degree_planning_search)
    else:
        raise ValueError('Invalid algorithm type')

    avg, points = calculate_avg(solution)
    print(f"Target points: {target_points}")
    print(f"Mandatory points: {mandatory_points}")
    print(f"Average: {avg}")
    print(f"Points: {points}")
    print(f"Expanded: {degree_planning_search.expanded}")
    for semester in solution:
        print(semester)


if __name__ == '__main__':
    main()
