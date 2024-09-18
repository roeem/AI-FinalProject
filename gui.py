import tkinter as tk
from tkinter import ttk


class GUI:
    def __init__(self, root, degree_plan):
        self.root = root
        self.root.title("Degree Plan Viewer")

        # Set a warm background color
        self.root.configure(bg="#f0e68c")  # Light khaki color

        # Configure grid layout for resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Frame to hold Treeview and scrollbars
        tree_frame = ttk.Frame(root)
        tree_frame.grid(row=0, column=0, sticky="nsew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Treeview for course details with an added "Semester" column
        self.tree = ttk.Treeview(tree_frame, columns=(
        "Number", "Name", "Semester", "Points", "Grade", "Mandatory", "Prerequisites"), show="headings")

        # Define headings, including semester after the course name
        self.tree.heading("Number", text="Course Number", anchor="center")
        self.tree.heading("Name", text="Course Name", anchor="center")
        self.tree.heading("Semester", text="Semester", anchor="center")
        self.tree.heading("Points", text="Points", anchor="center")
        self.tree.heading("Grade", text="Avg Grade", anchor="center")
        self.tree.heading("Mandatory", text="Mandatory", anchor="center")
        self.tree.heading("Prerequisites", text="Prerequisites", anchor="center")

        # Center column data and adjust column width
        self.tree.column("Number", anchor="center", width=100)
        self.tree.column("Name", anchor="center", width=250)
        self.tree.column("Semester", anchor="center", width=100)
        self.tree.column("Points", anchor="center", width=80)
        self.tree.column("Grade", anchor="center", width=80)
        self.tree.column("Mandatory", anchor="center", width=100)
        self.tree.column("Prerequisites", anchor="center", width=500)

        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)

        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Frame for summary details
        summary_frame = ttk.Frame(root, style="Summary.TFrame")
        summary_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.show_summary(degree_plan, summary_frame)

        # Populate the Treeview with course data
        self.populate_table(degree_plan)

    def show_summary(self, degree_plan, frame):
        # Use bold font for labels
        bold_font = ("TkDefaultFont", 10, "bold")

        # Display total points, mandatory points, average grade, semesters in bold
        ttk.Label(frame, text=f"Total Points: {degree_plan.total_points}", font=bold_font).grid(row=0, column=0,
                                                                                                padx=10, pady=5,
                                                                                                sticky="w")
        ttk.Label(frame, text=f"Mandatory Points: {degree_plan.mandatory_points}", font=bold_font).grid(row=0, column=1,
                                                                                                        padx=10, pady=5,
                                                                                                        sticky="w")
        ttk.Label(frame, text=f"Average Grade: {degree_plan.avg_grade:.2f}", font=bold_font).grid(row=0, column=2,
                                                                                                  padx=10, pady=5,
                                                                                                  sticky="w")
        ttk.Label(frame, text=f"Semesters: {len(degree_plan._LocalDegreePlan__semesters)}", font=bold_font).grid(row=0,
                                                                                                            column=3,
                                                                                                            padx=10,
                                                                                                            pady=5,
                                                                                                            sticky="w")

    def populate_table(self, degree_plan):
        for i, semester in enumerate(degree_plan._LocalDegreePlan__semesters):
            semester_type = "A" if i % 2 == 0 else "B"
            for course in sorted(semester, key=lambda c: c.number):
                # Insert a row for each course, including the semester number (A or B)
                self.tree.insert("", "end",
                                 values=(course.number, course.name, semester_type, course.points, course.avg_grade,
                                         "Yes" if course.is_mandatory else "No", course.prerequisites))
            # Insert a bold line after each semester (visual separator)
            self.tree.insert("", "end", values=("", "", "----------", "", "", "", ""))


def run_gui(degree_plan):
    root = tk.Tk()

    # Style configuration
    style = ttk.Style(root)

    # Configure Treeview style
    style.configure("Treeview.Heading", font=("TkDefaultFont", 10, "bold"))  # Bold font for headers
    style.configure("Treeview", rowheight=30, background="#faebd7", fieldbackground="#faebd7",
                    foreground="black")  # Warm background
    style.configure("Treeview", borderwidth=1, relief="solid")  # Vertical lines between columns
    style.map("Treeview", background=[("selected", "#e0e0e0")])  # Selection background

    # Configure vertical lines between columns
    style.configure("Treeview", highlightthickness=1, bd=1, relief="solid")

    # Configure row height and enable resizing
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Configure other elements
    style.configure("TLabel", background="#f0e68c")  # Warm background for labels

    gui = GUI(root, degree_plan)
    root.mainloop()