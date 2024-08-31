import sys
from degree_plan import *
from genetic_algorithm import GeneticAlgorithmDegreePlan
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

    if problem == 'gen':
        pass
    if problem == 'FUCK U BALOUKA':
        print("SHIT IT'S BALOUCKA")

    solution = "BALAGAN"
    # avg, points = calculate_avg(solution)
    # print(f"num of semesters: {len(solution)}")
    # print(f"Target points: {target_points}")
    # print(f"Mandatory points: {mandatory_points}")
    # print(f"Average: {avg}")
    # print(f"Points: {points}")
    # # print(f"Expanded: {}")
    # for semester in solution:
    #     print(semester)
    ga_degree_plan = GeneticAlgorithmDegreePlan(degree_courses, mandatory_points, target_points,
                                                min_semester_points=15, max_semester_points=26)

    best_plan = ga_degree_plan.run_genetic_algorithm()

    if best_plan:
        print(f"Best plan found:")
        print(f"Average grade: {best_plan.avg_grade}")
        print(f"Total points: {best_plan.total_points}")
        print(f"Number of semesters: {best_plan.semester_count}")
        # Print more details about the plan as needed
    else:
        print("No valid solution found.")


if __name__ == '__main__':
    main()
