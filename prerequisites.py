class Prerequisites:
    """
    Represents the prerequisites for a course as a Conjunctive Normal Form (CNF).
    Each clause in the CNF is a set of course numbers, where satisfying at least one course from each
    clause fulfills the prerequisites.

    For example, the prerequisites:
    {frozenset({1, 2, 3}), frozenset({2, 4}), frozenset({7})}
    means that to satisfy the prerequisites, the student must complete:
    (1 or 2 or 3) and (2 or 4) and (7).
    """

    def __init__(self, cnf_course_numbers: set[frozenset[int]] = None):
        """
        Initializes the Prerequisites object.

        :param cnf_course_numbers: A set of frozensets, each representing a clause of course numbers.
            To meet the prerequisites, at least one course from each frozenset must be completed.
            If None, there are no prerequisites.
        :type cnf_course_numbers: set[frozenset[int]], optional
        """
        self.__cnf_course_numbers = cnf_course_numbers

    def meets_prerequisites(self, course_numbers: set[int]) -> bool:
        """
        Checks if the given set of courses satisfies the prerequisites.

        :param course_numbers: A set of course numbers the student has completed.
        :type course_numbers: set[int]
        :return: True if the given courses satisfy all prerequisites, False otherwise.
        :rtype: bool
        """
        if self.__cnf_course_numbers is None:
            return True
        for clause in self.__cnf_course_numbers:
            for course_num in clause:
                if course_num in course_numbers:
                    break
            else:
                return False
        return True

    def __repr__(self):
        """
        Returns a string representation of the prerequisites.

        :return: A string showing the CNF of course prerequisites.
        :rtype: str
        """
        if self.__cnf_course_numbers is None:
            return "No Prerequisites"
        prereqs = []
        for clause in self.__cnf_course_numbers:
            clause_str = " or ".join(str(course_num) for course_num in sorted(clause))
            prereqs.append(f"({clause_str})")
        prereqs_str = " and ".join(prereqs)
        return f"[{prereqs_str}]"
