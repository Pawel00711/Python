#!/bin/bash
# Script to run the data processing Python program

# Define input, output, and report filenames
INPUT_FILE="students_grades.csv"
OUTPUT_FILE="student_results.csv"
REPORT_FILE="summary_report.txt"

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install Python3 to continue."
    exit 1
fi

# Execute the Python program with the correct arguments
echo "Running Data Processing Program..."
python3 data_processing.py "$INPUT_FILE" "$OUTPUT_FILE" "$REPORT_FILE"

echo "Program execution complete."
