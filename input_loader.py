import json

from course import Course
from prerequisites import Prerequisites


def load_degree_plan(json_file: str) -> tuple[int, int, list[Course]]:
    """
    Loads a degree plan from a JSON file and returns the total points of mandatory courses,
    the target points for the degree, and a list of courses.

    :param json_file: The path to the JSON file containing the degree plan.
    :type json_file: str
    :return: A tuple containing:
        - the total points for mandatory courses,
        - the target points for the degree,
        - a list of Course objects.
    :rtype: tuple[int, int, list[Course]]

    The JSON file is expected to have the following structure:
    .. code-block:: json

       {
           "target_points": int,
           "degree_courses": [
               {
                   "course_number": int,
                   "semester_type": "A" or "B",
                   "name": str,
                   "points": int,
                   "avg_grade": float,
                   "is_mandatory": bool,
                   "prerequisites": [[int]] (optional)
               },
               ...
           ]
       }
    """
    # Load JSON data from file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extract courses from the JSON data
    degree_courses = [
        Course(
            course_number=course_data['course_number'],
            semester_type=course_data['semester_type'],
            name=course_data['name'],
            points=course_data['points'],
            avg_grade=course_data['avg_grade'],
            is_mandatory=course_data['is_mandatory'],
            prerequisites=Prerequisites(
                set(map(frozenset, course_data.get('prerequisites', [])))) if course_data.get(
                'prerequisites') is not None else None
        )
        for course_data in data['degree_courses']
    ]

    # Calculate total mandatory points
    mandatory_courses = {(c.number, c.points) for c in degree_courses if c.is_mandatory}
    mandatory_points = sum(c[1] for c in mandatory_courses)

    return mandatory_points, data['target_points'], degree_courses
