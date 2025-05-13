# List or storage of student names
student_names = []

# List or storage of student ids
student_ids = []

# List of accepted values when recording attendance where p is present, a is absent, and e is excused
attendance = ["P", "A", "E"]

# List of days that will be recorded
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# List of weeks that will be recorded
weeks = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"]

# A dictionary where the attendance of each student will be recorded
attendance_records = {}

# Global variable to store the section name
section_name = ""

# Record function
def record():
    print(f"\nSection: {section_name}")
    print("Starting attendance recording (day by day)...")
    for week in weeks:
        print(f"\nRecording attendance for {week}...")
        for day in days:
            print(f"\nDay: {day}")
            for student in student_names:
                if student not in attendance_records:
                    attendance_records[student] = {}
                if week not in attendance_records[student]:
                    attendance_records[student][week] = {}

                while True:
                    status = input(f"Enter attendance for {student} on {week} - {day} (P = Present, A = Absent, E = Excused): ").capitalize()
                    if status in attendance:
                        attendance_records[student][week][day] = status
                        break
                    else:
                        print("Invalid input. Please enter P, A, or E.")

    # Calling the function to count the absences of each student
    check_absences()

# Update function
def update():
    print(f"\nSection: {section_name}")
    print("Updating attendance record for a specific student...")
    try:
        student_id_input = int(input("Enter the Student ID to update: "))
    except ValueError:
        print("Invalid input. Please enter a valid numeric ID.")
        return

    if student_id_input not in student_ids:
        print(f"Student ID '{student_id_input}' not found.")
        return

    index = student_ids.index(student_id_input)
    student_name = student_names[index]

    try:
        week_choice = int(input("Choose week (1-5): "))
        if not 1 <= week_choice <= 5:
            print("Week must be between 1 and 5.")
            return
        selected_week = weeks[week_choice - 1]

        day_choice = int(input("Choose day (1-5): "))
        if not 1 <= day_choice <= 5:
            print("Day must be between 1 and 5.")
            return
        selected_day = days[day_choice - 1]

        current_status = attendance_records.get(student_name, {}).get(selected_week, {}).get(selected_day, "None")
        print(f"Current status for {student_name} on {selected_week} - {selected_day}: {current_status}")

        new_status = input(f"Update {student_name} {selected_week} {selected_day} (P = Present, A = Absent, E = Excused): ").capitalize()
        if new_status not in attendance:
            print("Invalid status entered.")
            return

        if student_name not in attendance_records:
            attendance_records[student_name] = {}
        if selected_week not in attendance_records[student_name]:
            attendance_records[student_name][selected_week] = {}

        attendance_records[student_name][selected_week][selected_day] = new_status
        print(f"Attendance updated for {student_name} on {selected_week} - {selected_day}: {new_status}")

        # Calling the function to count the number of absences of each student
        check_absences()
    except ValueError:
        print("Invalid numeric input. Please enter numbers only for week/day.")
    except KeyError:
        print("Could not locate the attendance record. Please check your inputs.")

# Save attendance function
def save():
    import os
    import csv

    os.makedirs("records", exist_ok=True)
    file_path = os.path.join("records", "attendance_records.csv")

    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Header
            writer.writerow(["Section", "Student Name", "Week", "Day", "Status"])
            
            for student, weekly_records in attendance_records.items():
                for week, daily_records in weekly_records.items():
                    for day, status in daily_records.items():
                        writer.writerow([section_name, student, week, day, status])
        
        print(f"Attendance records saved to {file_path}")
    except IOError:
        print("Error saving file. Please check permissions or disk space.")

# Exit function
def exit_program():
    print("Exiting the system. Goodbye!")
    exit()

# Checking absences function
def check_absences():
    print("\nChecking absences...")
    for student, weekly_records in attendance_records.items():
        absences = sum(
            1 for week in weekly_records.values() for status in week.values() if status == "A"
        )
        if absences >= 10:
            print(f"{student} has been absent for two weeks. Status: FAILED.")
        elif absences >= 5:
            print(f"{student} has 5 absences. Status: SECOND WARNING.")
        elif absences >= 3:
            print(f"{student} has 3 absences. Status: FIRST WARNING.")
        else:
            print(f"{student} has no warnings. Status: OK.")

# Main function
def main():
    global section_name
    print("Welcome to the Attendance Management System!")
    section_name = input("Please enter the name of the section you will track: ")

    print(f"Please enter the names and IDs of the students of {section_name}. Type 'done' when you are finished.")

    while True:
        first_name = input("Enter the first name of the student (type 'done' if finish): ")
        if first_name.lower() == 'done':
            break
        last_name = input("Enter the last name of the student: ")

        try:
            student_id = int(input("Enter the student ID: "))
        except ValueError:
            print("Invalid input. Student ID must be a number.")
            continue

        full_name = f"{first_name} {last_name}"
        if full_name in student_names:
            print(f"Error: Student name '{full_name}' already exists.")
            continue
        if student_id in student_ids:
            print(f"Error: Student ID '{student_id}' already exists.")
            continue

        student_ids.append(student_id)
        student_names.append(full_name)
        print(f"Student {full_name} with ID {student_id} added.")

    while True:
        print("\nMenu:")
        print("1. Record Attendance")
        print("2. Save Attendance Records")
        print("3. Update Attendance Records")
        print("4. Exit")
        choice = input("Please enter your choice (1-4): ")

        if choice == "1":
            record()
        elif choice == "2":
            save()
        elif choice == "3":
            update()
        elif choice == "4":
            exit_program()
        else:
            print("Invalid choice. Please try again.")

# Start the program
main()