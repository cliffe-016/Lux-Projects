import csv

def grader():
    try:
        # Initialize an empty dictionary to store the inputs temporarily
        grades = {}

        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        student = f"{first_name} {last_name}"

        # Convert grade to float and handle input errors graefully
        try:
            student_grade = float(input("Enter grade: "))
        except ValueError:
            print("Invalid input")
            return

        # Define dictionary key and value
        grades['student'] = student
        grades['grade'] = student_grade

        # Store the inputs in a csv file
        with open("grades.csv", "a", newline="") as file:
            write = csv.writer(file)
            write.writerow(grades.values())
        print("Data stored successfully")

        # Initialize an empty list to store results from csv
        csv_data = []

        # Read the csv file to extract highest/lowest value
        with open("grades.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    csv_data.append(row[1])
        if csv_data:
            highest_grade = max(csv_data)
            lowest_grade = min(csv_data)
        print("Highest grade: ", highest_grade, "Lowest grade: ", lowest_grade)
    except FileNotFoundError:
        print("File not found")
    except PermissionError:
        print("Permission error")
    except csv.Error as e:
        print("csv Error: ", e)


if __name__ == "__main__":
    grader()
