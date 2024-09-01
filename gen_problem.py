import sys
from genetic_algorithm import *
from input_loader import load_degree_plan


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
    input_file_path = "input_files/" + sys.argv[1]
    min_semester_points = int(sys.argv[2])
    max_semester_points = int(sys.argv[3])

    mandatory_points, target_points, degree_courses = load_degree_plan(input_file_path)

    gen_problem_params = {
        'degree_courses': degree_courses,
        'target_points': target_points,
        'mandatory_points': mandatory_points,
        'min_semester_points': min_semester_points,
        'max_semester_points': max_semester_points,
        'population_size': 50,
        'max_generations': 100,
        'mutation_rate': 0.1
    }

    gen_degree_plan = GeneticAlgorithm(**gen_problem_params)

    best_solution = gen_degree_plan.run()
    print("Average grade: ", best_solution.avg_grade)
    print("Total points: ", best_solution.total_points)
    print("Mandatory points: ", best_solution.mandatory_points)
    print("Semesters: ", len(best_solution.semesters))

    for semester in best_solution.semesters:
        print(f"Semester AVG: {semester.avg_grade}")
        print(semester)

if __name__ == '__main__':
    main()
