import csv  # Importing CSV module to handle file reading/writing
import sys  # Importing sys module to handle program exit on critical errors
import argparse  # Importing argparse to handle command-line arguments
import os  # Importing os module for file existence checking

# Deliverables and Application Requirements Included
#
# This program reads student grades from a CSV file passed via the command line,
# processes their average scores, finds the highest and lowest scores,
# assigns letter grades, and outputs results to another CSV file.
# Additionally, a report summarizing processing activity is generated.

# Function to read student data from a CSV file

def read_student_data(filename):
    """Reads student data from a CSV file passed via the command line with error handling."""
    data = []
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' does not exist.")
        sys.exit(1)
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:
                if len(row) < 6:
                    print(f"Warning: Incomplete data in row: {row}")
                    continue
                try:
                    data.append({
                        'Name': row[0],
                        'Art': int(row[1]),
                        'Chemistry': int(row[2]),
                        'Science': int(row[3]),
                        'English': int(row[4]),
                        'Math': int(row[5])
                    })
                except ValueError as e:
                    print(f"Error: Invalid data in row {row}: {e}")
                    sys.exit(1)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    return data

def calculate_average(student):
    """Calculates the average score of a student."""
    total = sum([student['Art'], student['Chemistry'], student['Science'], student['English'], student['Math']])
    return total / 5

def find_highest_lowest(student):
    """Finds the highest and lowest scores for a student."""
    scores = [student['Art'], student['Chemistry'], student['Science'], student['English'], student['Math']]
    return max(scores), min(scores)

def assign_grade(score):
    """Assigns a letter grade based on score."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    elif score >= 50:
        return "E"
    else:
        return "F"

def process_student_results(students_data):
    """Processes student data to compute averages, highest/lowest scores, and grades."""
    results = []
    for student in students_data:
        average = calculate_average(student)
        highest, lowest = find_highest_lowest(student)
        results.append({
            'Name': student['Name'],
            'Art': student['Art'],
            'Chemistry': student['Chemistry'],
            'Science': student['Science'],
            'English': student['English'],
            'Math': student['Math'],
            'Average': average,
            'Highest_Score': highest,
            'Lowest_Score': lowest,
            'Overall_Grade': assign_grade(average),
            'Art_Grade': assign_grade(student['Art']),
            'Chemistry_Grade': assign_grade(student['Chemistry']),
            'Science_Grade': assign_grade(student['Science']),
            'English_Grade': assign_grade(student['English']),
            'Math_Grade': assign_grade(student['Math'])
        })
    return results

def write_results_to_csv(results, filename):
    """Writes student results to an output CSV file with error handling."""
    try:
        if results:
            header = ['Name', 'Art', 'Chemistry', 'Science', 'English', 'Math', 'Average', 'Highest_Score', 'Lowest_Score', 'Overall_Grade', 'Art_Grade', 'Chemistry_Grade', 'Science_Grade', 'English_Grade', 'Math_Grade']
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writeheader()
                writer.writerows(results)
            print(f"Results successfully written to {filename}")
        else:
            print("No results to write.")
    except Exception as e:
        print(f"Error: Failed to write to {filename}: {e}")
        sys.exit(1)

def generate_summary_report(results, report_filename):
    """Generates a summary report of the processing activity with error handling."""
    try:
        total_students = len(results)
        highest_avg = max(results, key=lambda x: x['Average'])
        lowest_avg = min(results, key=lambda x: x['Average'])
        
        with open(report_filename, 'w', encoding='utf-8') as file:
            file.write("Summary Report\n")
            file.write("====================\n")
            file.write(f"Total Students Processed: {total_students}\n")
            file.write(f"Highest Average Score: {highest_avg['Name']} - {highest_avg['Average']}\n")
            file.write(f"Lowest Average Score: {lowest_avg['Name']} - {lowest_avg['Average']}\n")
        
        print(f"Summary report successfully written to {report_filename}")
    except Exception as e:
        print(f"Error: Failed to write report to {report_filename}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process student grades from a CSV file.")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("output_file", help="Path to the output CSV file")
    parser.add_argument("report_file", help="Path to the summary report file")
    args = parser.parse_args()
    
    students_data = read_student_data(args.input_file)
    results = process_student_results(students_data)
    write_results_to_csv(results, args.output_file)
    generate_summary_report(results, args.report_file)
    print("Processing complete. Goodbye!")
