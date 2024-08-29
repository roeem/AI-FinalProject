import json
import math

from course import Course
from degree_planning_problems import DegreePlanningMinTime
from prerequisites import Prerequisites


def load_degree_plan(json_file: str, min_semester_points: int = 0, max_semester_points: int = math.inf) -> (
        DegreePlanningMinTime):
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
            avg_grade=course_data['avg_grade'],
            is_mandatory=course_data['is_mandatory'],
            prerequisites=Prerequisites(
                set(map(frozenset, course_data.get('prerequisites', [])))) if course_data.get(
                'prerequisites') is not None else None
        )
        for course_data in data['degree_courses']
    )

    # Create the DegreePlan object
    degree_planning_search = DegreePlanningMinTime(
        degree_courses=degree_courses,
        mandatory_points=data['mandatory_points'],
        target_points=data['target_points'],
        min_semester_points=min_semester_points,
        max_semester_points=max_semester_points
    )
    return degree_planning_search
