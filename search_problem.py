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


def get_upper_bound_avg(courses: list[Course], total_points: int) -> float:
    mandatory_courses = {}
    for course in courses:
        if course.is_mandatory:
            if course.number in mandatory_courses:
                mandatory_courses[course.number] = max([mandatory_courses[course.number], course], key=lambda x: x.avg_grade)
            else:
                mandatory_courses[course.number] = course

    weighted_sum_mandatory = sum([course.avg_grade * course.points for course in mandatory_courses.values()])
    sum_mandatory_points = sum([course.points for course in mandatory_courses.values()])

    elective_courses = {}
    for course in courses:
        if not course.is_mandatory:
            if course.number in elective_courses:
                elective_courses[course.number] = max([elective_courses[course.number], course], key=lambda x: x.avg_grade)
            else:
                elective_courses[course.number] = course

    # Sort elective courses by avg grade in descending order
    elective_courses = sorted(elective_courses.values(), key=lambda x: x.avg_grade)

    sum_elective_points = 0
    weighted_elective_sum = 0
    while sum_elective_points < total_points - sum_mandatory_points:
        course = elective_courses.pop()
        sum_elective_points += course.points
        weighted_elective_sum += course.avg_grade * course.points

    total_average = (weighted_sum_mandatory + weighted_elective_sum) / (sum_mandatory_points + sum_elective_points)
    return total_average


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

    # print("Suprimum avg: ", get_suprimum_avg(list(degree_courses), target_points))
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
    print(f"Average: {avg}")
    print(f"Points: {points}")
    print(f"Expanded: {degree_planning_search.expanded}")
    for course in solution:
        print(course)


if __name__ == '__main__':
    main()
