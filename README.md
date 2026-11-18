# Week 1 assessment · Python and data engineering

Run `python3 task1.py` from the repository directory. Python 3.6 or newer is sufficient. The script reads the eight supplied records from `employees.csv` beside the script.

Salary is treated as monthly pay, so Arun's 30,000 gives an annual salary of 360,000. The manager and negative-salary examples use separate demonstration records because the CSV contains neither team sizes nor negative salaries.

The name and city filters use the original CSV. The raise is calculated in memory for each employee. In file order, the salary scan skips zero pay and includes the first employee above 85,000 before stopping. With the supplied data that employee is Karthik.

## Task 2 · Files and APIs

From the repository root, create a virtual environment with `python -m venv .venv`.
On Windows run `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.
Create a local .env in the root containing `API_KEY=practice-only`, then run
`.\.venv\Scripts\python.exe task_2/task_2.py`. On Linux use `.venv/bin/python` for both commands.

The script reads the CSV inside task_2 and writes its three exports beside it.
Employee IDs and salaries are JSON numbers. users.json includes all returned users
and their address.city values. Only the first three users appear on screen.
JSONPlaceholder is public. The practice key demonstrates configuration loading and stays local.

## Task 3 · Marks and employee analysis

From the project root on Windows, run `.\.venv\Scripts\python.exe task_3/task_3.py`.
On Linux run `.venv/bin/python task_3/task_3.py`. Task 3 reads employees.csv
beside the script and produces its CSV files, four PNGs and insights.txt there.

The example uses original marks and subject weights of 40%, 35% and 25%.
For the cleaning exercise, Priya and Meena have missing pay and Arun appears
twice in employees_raw.csv. Removing the duplicate first gives each employee one
vote in the median. Department heads and budgets are example values. Joins
start from the department directory so the left join also shows empty departments.
