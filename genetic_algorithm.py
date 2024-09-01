import random
from degree_plan import DegreePlan, Semester
from course import Course


class GeneticAlgorithm:
    def __init__(self, degree_courses: frozenset[Course], target_points: int, mandatory_points,
                 min_semester_points: int, max_semester_points: int,
                 population_size: int = 50, max_generations: int = 100, mutation_rate: float = 0.1):

        self.degree_courses: frozenset[Course] = degree_courses
        self.population_size: int = population_size
        self.max_generations: int = max_generations
        self.mutation_rate: float = mutation_rate
        self.population: list[DegreePlan] = []
        self.min_semester_points: int = min_semester_points
        self.max_semester_points: int = max_semester_points
        self.target_points: int = target_points
        self.mandatory_points: int = mandatory_points

    def initialize_population(self) -> None:
        for _ in range(self.population_size):
            degree_plan = DegreePlan(self.degree_courses)

            while degree_plan.total_points < self.target_points:  # required_points needs to be defined
                possible_semesters = degree_plan.get_legal_semesters(self.min_semester_points, self.max_semester_points)
                if possible_semesters:
                    chosen_semester = random.choice(possible_semesters)
                else:
                    chosen_semester = self.create_arbitrary_semester(degree_plan.get_optional_courses(),
                                                                     degree_plan.next_semester_type)
                degree_plan = degree_plan.add_semester(chosen_semester)

            self.population.append(degree_plan)

    def create_arbitrary_semester(self, courses: frozenset[Course], semester_type: str) -> Semester:
        current_semester_courses, points, break_threshold = set(), 0, len(courses)
        courses = [course for course in courses if course.semester_type == semester_type]
        while points < self.min_semester_points:
            course_ind = random.randint(0, len(courses) - 1)
            course = courses[course_ind]
            if course.points + points <= self.max_semester_points:
                current_semester_courses.add(course)
                points += course.points
                courses.pop(course_ind)

            break_threshold -= 1
            if break_threshold == 0:
                break
        return Semester(frozenset(current_semester_courses), semester_type)

    def calculate_fitness(self, degree_plan: DegreePlan) -> float:  # TODO: check
        if degree_plan.total_points >= self.target_points and degree_plan.mandatory_points >= self.mandatory_points:
            return degree_plan.avg_grade
        else:
            penalty = abs(self.target_points - degree_plan.total_points) * 0.1
            return degree_plan.avg_grade - penalty

    def tournament_selection(self, k: int = 3) -> DegreePlan:
        pool: list[DegreePlan] = random.sample(self.population, k)
        return max(pool, key=self.calculate_fitness)

    def crossover(self, parent1: DegreePlan, parent2: DegreePlan) -> DegreePlan:
        if parent1.semester_count < 2 or parent2.semester_count < 2:
            return random.choice([parent1, parent2])

        crossover_point = random.randint(1, min(parent1.semester_count, parent2.semester_count) - 1)
        parent1_semesters, parent2_semesters = parent1.semesters, parent2.semesters
        child_semesters = parent1_semesters[:crossover_point] + parent2_semesters[crossover_point:]
        return DegreePlan(self.degree_courses, child_semesters)

    def mutation_add(self, degree_plan: DegreePlan) -> DegreePlan:
        pass

    def mutation_remove(self, degree_plan: DegreePlan) -> DegreePlan:
        pass

    def mutation_replace(self, degree_plan: DegreePlan) -> DegreePlan:
        pass

    def mutate(self, degree_plan: DegreePlan) -> DegreePlan:
        return degree_plan
        # if random.random() < self.mutation_rate:
        #     # Copy the degree plan to avoid modifying the original during experimentation
        #     mutated_plan = degree_plan.__copy__()
        #
        #     # Select a random semester to mutate
        #     if mutated_plan.semesters:
        #         semesters = list(mutated_plan.semesters)
        #         semester_to_mutate = random.choice(semesters)
        #         courses = list(semester_to_mutate.courses)
        #
        #         # Decide on the mutation operation
        #         mutation_type = random.choice(['add', 'remove', 'replace']) if courses else 'add'
        #         if mutation_type == 'add':
        #             potential_additions = [course for course in self.degree_courses if
        #                                    course.semester_type == semester_to_mutate.semester_type
        #                                    and course not in courses and mutated_plan.can_take_this_course(course)]
        #             if potential_additions:
        #                 course_to_add = random.choice(potential_additions)
        #                 courses.append(course_to_add)
        #         elif mutation_type == 'remove':
        #             # Ensure that no course being removed is a prerequisite for another course in the future semesters
        #             valid_removals = [course for course in courses if not any(
        #                 course.number in future_course.prerequisites for future_semester in semesters for future_course
        #                 in future_semester.courses if future_semester != semester_to_mutate)]
        #             if valid_removals:
        #                 courses.remove(random.choice(valid_removals))
        #         elif mutation_type == 'replace':
        #             # Replace a random course with another
        #             valid_replacements = [course for course in courses if not any(
        #                 course.number in future_course.prerequisites for future_semester in semesters for future_course
        #                 in future_semester.courses if future_semester != semester_to_mutate)]
        #             if valid_replacements:
        #                 course_to_replace = random.choice(valid_replacements)
        #                 potential_replacements = [course for course in self.degree_courses if
        #                                           course.semester_type == semester_to_mutate.semester_type
        #                                           and course not in courses and mutated_plan.can_take_this_course(
        #                                               course)]
        #                 if potential_replacements:
        #                     replacement_course = random.choice(potential_replacements)
        #                     index = courses.index(course_to_replace)
        #                     courses[index] = replacement_course
        #
        #         # Create a new semester with the mutated list of courses
        #         new_semester = Semester(frozenset(courses), semester_to_mutate.semester_type)
        #         mutated_plan.replace_semester(semester_to_mutate, new_semester)
        #
        #     return mutated_plan
        # return degree_plan

    def condition_met(self, best_solution):
        return False

    def run(self) -> DegreePlan:
        self.initialize_population()
        best_solution: DegreePlan = None
        for generation in range(self.max_generations):
            new_population: list[DegreePlan] = []
            for _ in range(len(self.population)):
                mommy, daddy = self.tournament_selection(), self.tournament_selection()
                child = self.crossover(mommy, daddy)
                child = self.mutate(child) if random.random() < self.mutation_rate else child
                new_population.append(child)

            self.population = new_population
            current_best = max(self.population, key=self.calculate_fitness)
            if best_solution:
                best_solution = max(best_solution, current_best, key=self.calculate_fitness)
            else:
                best_solution = current_best

            if self.condition_met(best_solution):
                break
        return best_solution
