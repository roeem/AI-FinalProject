import pygad
import numpy as np
from typing import List, Dict, Set
from course import Course
from degree_plan import DegreePlan, Semester
from prerequisites import Prerequisites


class GeneticAlgorithmDegreePlan:
    def __init__(self, degree_courses: Set[Course], mandatory_points: int, target_points: int,
                 min_semester_points: int, max_semester_points: int):
        self.degree_courses = list(degree_courses)
        self.mandatory_points = mandatory_points
        self.target_points = target_points
        self.min_semester_points = min_semester_points
        self.max_semester_points = max_semester_points
        self.course_dict = {course.number: course for course in degree_courses}

    def initialize_population(self):
        # Initialize a random population
        num_courses = len(self.degree_courses)
        return np.random.randint(0, 12, size=(100, num_courses))

    def fitness_func(self, solution, solution_idx):
        # Convert the solution to a DegreePlan
        degree_plan = self.solution_to_degree_plan(solution)

        if degree_plan is None:
            return 0  # Invalid solution

        # Calculate fitness based on average grade and satisfaction of constraints
        avg_grade = degree_plan.avg_grade
        total_points = degree_plan.total_points
        mandatory_points = sum(
            course.points for course in degree_plan._DegreePlan__courses_so_far.values() if course.is_mandatory)

        # Penalize solutions that don't meet constraints
        if total_points < self.target_points or mandatory_points < self.mandatory_points:
            return 0

        return avg_grade

    def solution_to_degree_plan(self, solution) -> DegreePlan:
        degree_plan = DegreePlan(frozenset(self.degree_courses))
        courses_taken = set()

        for semester in range(1, 13):  # Assume max 12 semesters
            semester_courses = []
            semester_points = 0

            for i, course_semester in enumerate(solution):
                if course_semester == semester:
                    course = self.degree_courses[i]
                    if not self.is_course_valid(course, courses_taken, semester):
                        continue

                    semester_courses.append(course)
                    semester_points += course.points

                    if semester_points > self.max_semester_points:
                        break

            if self.min_semester_points <= semester_points <= self.max_semester_points:
                new_semester = Semester(frozenset(semester_courses), 'A' if semester % 2 else 'B')
                degree_plan = degree_plan.add_semester(new_semester)
                courses_taken.update(course.number for course in semester_courses)
            elif semester_courses:
                return None  # Invalid solution

        return degree_plan

    def is_course_valid(self, course: Course, courses_taken: Set[int], semester: int) -> bool:
        if course.number in courses_taken:
            return False
        if course.semester_type != ('A' if semester % 2 else 'B'):
            return False
        if not course.prerequisites.meets_prerequisites(courses_taken):
            return False
        return True

    def run_genetic_algorithm(self):
        num_generations = 100
        num_parents_mating = 4

        ga_instance = pygad.GA(num_generations=num_generations,
                               num_parents_mating=num_parents_mating,
                               fitness_func=self.fitness_func,
                               num_genes=len(self.degree_courses),
                               sol_per_pop=100,
                               init_range_low=0,
                               init_range_high=12,
                               mutation_percent_genes=10,
                               mutation_type="random",
                               mutation_by_replacement=True,
                               random_mutation_min_val=0,
                               random_mutation_max_val=12)

        ga_instance.run()

        solution, solution_fitness, _ = ga_instance.best_solution()
        best_degree_plan = self.solution_to_degree_plan(solution)

        return best_degree_plan