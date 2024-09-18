from local_search.local_degree_plan import LocalDegreePlan
from local_search.local_degree_planning_problem import LocalDegreePlanningProblem
from local_search.local_search_ import *
import time


def tests(degree_courses, mandatory_points, max_semester_points, min_semester_points, target_points):
    dpp = LocalDegreePlanningProblem(degree_courses, mandatory_points, target_points, min_semester_points,
                                     max_semester_points)
    states = []
    for _ in range(10):
        states.append(dpp.get_initial_state())
    states.sort(key=lambda x: dpp.fitness(x))
    for s in states:
        print(f"Fitness Score= {dpp.fitness(s)}\n The Degree Plan:\n{s}\n")
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
                    # start_time = time.time()
                    solution: LocalDegreePlan = (
                        simulated_annealing(dpp, schedule=lambda t: exp_cool_schedule(t, T0, alpha), eps=eps))
                    # total_time = time.time() - start_time
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
        if is_valid_degree_plan(solution, degree_planning_search_params):
            print(f"SUCCESSSSSSSSSSSSSSSSS")
    avg_expanded = expanded / number_of_runs
    legal_runs_avg = [run[0].avg_grade for run in runs if
                      is_valid_degree_plan(run[0], degree_planning_search_params)]
    avg_avg_grade = sum(legal_runs_avg) / len(legal_runs_avg)
    legal_ratio = len(legal_runs_avg) / number_of_runs

    print(f"Average Average Grade: {avg_avg_grade}")
    print(f"Legal Ratio: {legal_ratio}")
    print(f"Average Expanded: {avg_expanded}")
    return avg_avg_grade, legal_ratio


def is_valid_degree_plan(degree_plan: LocalDegreePlan, degree_planning_params):
    if degree_plan.total_points != degree_planning_params['target_points']:
        return False
    if degree_plan.mandatory_points != degree_planning_params['mandatory_points']:
        return False
    return True
