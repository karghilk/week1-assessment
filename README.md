# Week 1 assessment · Task 1

Run `python3 task1.py` from the repository directory. Python 3.6 or newer is sufficient. The script reads the eight supplied records from `employees.csv` beside the script.

Salary is treated as monthly pay, so Arun's 30,000 gives an annual salary of 360,000. The manager and negative-salary examples use separate demonstration records because the CSV contains neither team sizes nor negative salaries.

The name and city filters use the original CSV. The raise is calculated in memory for each employee. In file order, the salary scan skips zero pay and includes the first employee above 85,000 before stopping. With the supplied data that employee is Karthik.
