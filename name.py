import csv
import os

import statistics

from typing import List, Dict, Any

SUBJECTS = ["English", "Maths", "Science","Social", "Human Values"]


def validate_mark(mark_str):
    try:
        mark_as_int=int(mark_str)
    except ValueError:
        raise ValueError("Mark must be an integer.")
    if not (0<= mark_as_int<= 100):
        raise ValueError("Mark must be between 0 and 100.")
    return mark_as_int

def assign_grade(percentage):
    if percentage >=90:
        return "A+"
    if percentage >=80:
        return "A"
    if percentage >=70:
        return "B+"
    if percentage >=60:
        return "B"
    if percentage >=50:
        return "C"
    if percentage >= 40:
        return "D"
    return "F"

def input_student(subjects:list):
    name=input("Enter student name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name=input("Enter student name: ").strip()

    roll_no=input("Enter roll number (optional): ").strip()
    marks=[]
    for subj in subjects:
        while True:
            try:
                raw=input(f"Enter marks for {subj} (0-100): ").strip()
                mark_as_int=validate_mark(raw)
                marks.append(mark_as_int)
                break
            except ValueError as e:
                print("Invalid mark:", e)

    total=sum(marks)
    percentage=total / len(subjects) if subjects else 0.0
    grade=assign_grade(percentage)
    student={
        "name":name,
        "roll_no":roll_no,
        "marks":marks,
        "total":total,
        "percentage":round(percentage, 2),
        "grade":grade
    }
    return student


def format_report_card(student:dict, subjects:list):
    header=f"Report Card - {student['name']}"
    if student['roll_no']:
        header+=f" (Roll: {student['roll_no']})"
    lines=[header, "-" * len(header)]
    for subj, mark in zip(subjects, student["marks"]):
        lines.append(f"{subj:<12}: {mark:>3}")
    lines.append("-" * 23)
    lines.append(f"Total      :{student['total']}")
    lines.append(f"Percentage :{student['percentage']}%度の")
    lines.append(f"Grade      :{student['grade']}")
    return "\n".join(lines)


def save_students_to_csv(students: list ,subjects: list ,filename: str):
    fieldnames=["name", "roll_no"] + subjects + ["total", "percentage", "grade"]
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in students:
            row={"name": s["name"], "roll_no": s["roll_no"],
                   "total": s["total"], "percentage": s["percentage"], "grade": s["grade"]}
            for subj, mark in zip(subjects, s["marks"]):
                row[subj]=mark
            writer.writerow(row)
    print(f"Saved {len(students)} students to {filename}")
def load_students_from_csv(filename: str, subject: list)->list:

    students=[]
    if not os.path.exists(filename):
        print("File not found:", filename)
        return students
    with open(filename, mode="r", newline="", encoding="utf-8") as f:
        reader=csv.DictReader(f)
        for row in reader:
            marks=[]
            for subj in subjects:
                val=row.get(subj, "")
                try:
                    marks.append(int(val))
                except (ValueError, TypeError):
                    marks.append(0)
            total=int(row.get("total", sum(marks)))
            percentage=float(row.get("percentage", 0.0))
            students.append({
                "name":row.get("name", "").strip(),
                "roll_no":row.get("roll_no", "").strip(),
                "marks":marks,
                "total":total,
                "percentage":round(percentage, 2),
                "grade":row.get("grade", "").strip()
            })
    print(f"Loaded {len(students)} students from {filename}")
    return students

def export_individual_reports(students: list, subjects : list ,folder: str = "report_cards"):
    os.makedirs(folder, exist_ok=True)
    for s in students:
        safe_name = "".join(c if c.isalnum() or c in " -_" else "_" for c in s["name"])
        filename = os.path.join(folder, f"{safe_name}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(format_report_card(s, subjects))
    print(f"Exported {len(students)} report(s) to folder '{folder}'.")

def class_statistics(students: list)->dict:
    """Return some class-level statistics: average percentage, highest, lowest, pass rate."""
    if not students:
        return {}
    percentages = [s["percentage"] for s in students]
    totals=[s["total"] for s in students]
    grades=[s["grade"] for s in students]
    avg_percent =round(statistics.mean(percentages), 2)
    highest=max(percentages)
    lowest =min(percentages)
    top_students =[s["name"] for s in students if s["percentage"] == highest]
    fail_count =sum(1 for p in percentages if p < 40)
    pass_rate =round((1 - fail_count / len(students)) * 100, 2)
    return {
        "average_percentage": avg_percent,
        "highest_percentage": highest,
        "lowest_percentage": lowest,
        "top_students": top_students,
        "pass_rate_percent": pass_rate
    }

def print_class_summary(stats: Dict):
    if not stats:
        print("No students to summarize.")
        return
    print("\nClass Summary")
    print("-------------")
    print(f"Average Percentage : {stats['average_percentage']}% ")
    print(f"Highest Percentage : {stats['highest_percentage']}% (Top: {', '.join(stats['top_students'])})")
    print(f"Lowest Percentage  : {stats['lowest_percentage']}% ")
    print(f"Class Pass Rate    : {stats['pass_rate_percent']}% ")
    print()


def find_student_by_name(students: list,name_query)->list:
    q = name_query.strip().lower()
    return [s for s in students if q in s["name"].lower()]


def simple_menu():
    print("\nStudent Marks & Report Card Generator")
    print("=====================================")


def main():
    subjects=SUBJECTS.copy()
    students=[]
    while True:
        simple_menu()
        print("Subjects:", ", ".join(subjects))
        print("1. Add a student")
        print("2. Add multiple students")
        print("3. View all students")
        print("4. Show a student's report card")
        print("5. Class summary / statistics")
        print("6. Save all students to CSV")
        print("7. Load students from CSV")
        print("8. Export individual report text files")
        print("9. Change subjects")
        print("0. Exit")
        choice=input("Choose an option: ").strip()
        if choice=="1":
            s = input_student(subjects)
            students.append(s)
            print("Student added.")
        elif choice=="2":
            try:
                n = int(input("How many students to add? ").strip())
            except ValueError:
                print("Please enter an integer.")
                continue
            for i in range(n):
                print(f"\nEntering student {i+1} of {n}")
                s = input_student(subjects)
                students.append(s)
            print(f"{n} students added.")
        elif choice=="3":
            if not students:
                print("No students available.")
                continue
            for idx, s in enumerate(students, start=1):
                print(f"{idx}. {s['name']} - {s['percentage']}% - {s['grade']}")
        elif choice=="4":
            if not students:
                print("No students available.")
                continue
            q = input("Enter student name to search:").strip()
            matches = find_student_by_name(students, q)
            if not matches:
                print("No matching student found.")
                continue
            for s in matches:
                print("\n" + format_report_card(s, subjects) + "\n")
        elif choice=="5":
            stats = class_statistics(students)
            print_class_summary(stats)
        elif choice=="6":
            if not students:
                print("No students to save.")
                continue
            fn = input("Enter filename (default students.csv):").strip() or "students.csv"
            save_students_to_csv(students, subjects, fn)
        elif choice=="7":
            fn = input("Enter filename to load (default students.csv):").strip() or "students.csv"
            loaded = load_students_from_csv(fn, subjects)
            if loaded:
                students.extend(loaded)
        elif choice=="8":
            if not students:
                print("No students to export.")
                continue
            folder=input("Enter folder name for reports (default 'report_cards'):").strip() or "report_cards"
            export_individual_reports(students, subjects, folder)
        elif choice=="9":
            print("Current subjects:", ", ".join(subjects))
            new = input("Enter subjects separated by commas (or leave empty to keep):").strip()
            if new:
                parts = [p.strip() for p in new.split(",") if p.strip()]
                if parts:
                    subjects = parts
                    print("Subjects updated.")
                else:
                    print("No valid subjects entered; keeping existing.")
        elif choice=="0":
            print("seems like you don't have data to enter")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
