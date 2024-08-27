class Prerequisites:
    """
    This class represent Prerequisites for some course.
    Prerequisites object is like CNF - every clause is 'or' courses.
    For example - the Prerequisites: {frozenset({1,2,3}),frozenset({2,4}),frozenset({7})} means that
    the prerequisites are the following:
    (1 or 2 or 3) and (2 or 4) and (7).
    """
    def __init__(self, cnf_course_numbers: set[frozenset[int]] = None):
        """
        :param cnf_course_numbers: set contains the prerequisite course numbers.
        To meet the prerequisites you have to take at least one course from each group.
        """
        self.__cnf_course_numbers = cnf_course_numbers

    def meets_prerequisites(self, courses: set[int]) -> bool:
        """
        Checks if the courses in the set are sufficient to meet the prerequisites
        :param courses: set of course numbers.
        :return: True if and only if these courses are satisfies the prerequisites.
        """
        if self.__cnf_course_numbers is None:
            return True

        for clause in self.__cnf_course_numbers:
            for course_num in clause:
                if course_num in courses:
                    break
            else:
                return False
        return True

    def __repr__(self):
        """
        For debugging
        """
        if self.__cnf_course_numbers is None:
            return "No Prerequisites"
        prereqs = []
        for clause in self.__cnf_course_numbers:
            clause_str = " or ".join(str(course_num) for course_num in sorted(clause))
            prereqs.append(f"({clause_str})")
        prereqs_str = " and ".join(prereqs)
        return f"{prereqs_str}"