import json
from course import Course
from degree_plan import DegreePlan
from prerequisites import Prerequisites


def load_degree_plan(json_file: str) -> DegreePlan:
    # Load JSON data from file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extract courses from the JSON data
    degree_courses = frozenset(
        Course(
            course_number=course_data['course_number'],
            semester_type=course_data['semester_type'],
            name=course_data['name'],
            points=course_data['points'],
            is_mandatory=course_data['is_mandatory'],
            prerequisites=Prerequisites(set(map(frozenset, course_data['prerequisites'])))
        )
        for course_data in data['degree_courses']
    )

    # Create the DegreePlan object
    degree_plan = DegreePlan(
        degree_courses=degree_courses,
        mandatory_courses_points=data['mandatory_courses_points'],
        min_degree_points=data['min_degree_points'],
        min_semester_points=data['min_semester_points'],
        max_semester_points=data['max_semester_points']
    )
    return degree_plan
