def generate_html(degree_plan, filename="degree_plan.html"):
    # HTML header and styles
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Degree Plan Viewer</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #faf3e0;
                margin: 0;
                padding: 0;
                color: #333;
            }}

            header {{
                background-color: #f0e68c;
                padding: 20px;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                letter-spacing: 1px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}

            .container {{
                max-width: 1200px;
                margin: 40px auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            }}

            h2 {{
                color: #2c3e50;
                font-size: 28px;
                margin-bottom: 10px;
            }}

            .summary {{
                display: flex;
                justify-content: space-between;
                padding: 20px;
                background-color: #f7d794;
                border-radius: 8px;
                margin-bottom: 20px;
                font-weight: bold;
            }}

            .summary div {{
                width: 24%;
                text-align: center;
                font-size: 18px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 40px;
            }}

            th, td {{
                padding: 12px 16px;
                text-align: center;
                border-bottom: 1px solid #ddd;
                font-size: 16px;
            }}

            th {{
                background-color: #f7d794;
                color: #333;
                font-weight: bold;
            }}

            tr:nth-child(even) {{
                background-color: #faf3e0;
            }}

            .semester-separator {{
                background-color: #f0e68c;
                color: #333;
                font-weight: bold;
                text-align: center;
            }}

            footer {{
                text-align: center;
                padding: 20px;
                background-color: #f0e68c;
                position: fixed;
                bottom: 0;
                width: 100%;
                font-size: 14px;
                letter-spacing: 1px;
            }}

            @media (max-width: 768px) {{
                .summary {{
                    flex-direction: column;
                }}

                .summary div {{
                    margin-bottom: 10px;
                    width: 100%;
                }}

                th, td {{
                    font-size: 14px;
                }}
            }}
        </style>
    </head>
    <body>

        <header>Degree Plan Viewer</header>

        <div class="container">

            <h2>Degree Plan Summary</h2>
            <div class="summary">
                <div>Total Points: {total_points}</div>
                <div>Mandatory Points: {mandatory_points}</div>
                <div>Average Grade: {avg_grade}</div>
                <div>Semesters: {num_semesters}</div>
            </div>

            <h2>Course Details</h2>
            <table>
                <thead>
                    <tr>
                        <th>Course Number</th>
                        <th>Course Name</th>
                        <th>Semester</th>
                        <th>Points</th>
                        <th>Avg Grade</th>
                        <th>Mandatory</th>
                        <th>Prerequisites</th>
                    </tr>
                </thead>
                <tbody>
    """.format(
        total_points=degree_plan.total_points,
        mandatory_points=degree_plan.mandatory_points,
        avg_grade=f"{degree_plan.avg_grade:.2f}",
        num_semesters=len(degree_plan._LocalDegreePlan__semesters)
    )

    # Loop through semesters and courses
    for i, semester in enumerate(degree_plan._LocalDegreePlan__semesters):
        semester_type = "A" if i % 2 == 0 else "B"
        for course in sorted(semester, key=lambda c: c.number):
            html_content += f"""
                <tr>
                    <td>{course.number}</td>
                    <td>{course.name}</td>
                    <td>{semester_type}</td>
                    <td>{course.points}</td>
                    <td>{course.avg_grade}</td>
                    <td>{"Yes" if course.is_mandatory else "No"}</td>
                    <td>{course.prerequisites}</td>
                </tr>
            """
        # Insert a separator between semesters
        html_content += """
            <tr class="semester-separator">
                <td colspan="7">---------- Semester End ----------</td>
            </tr>
        """

    # Close the HTML document
    html_content += """
                </tbody>
            </table>
        </div>

        <footer>
            Degree Plan Viewer &copy; 2024
        </footer>

    </body>
    </html>
    """

    # Write the HTML content to a file
    with open(filename, "w") as file:
        file.write(html_content)

    print(f"HTML file '{filename}' has been generated successfully.")
