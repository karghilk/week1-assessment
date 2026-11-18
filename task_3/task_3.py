from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


def marks_demo():
    # Columns are Maths, Science and English, in that order.
    marks = np.array([[80, 70, 90], [75, 85, 65], [90, 95, 85], [60, 75, 81]])
    weights = np.array([0.4, 0.35, 0.25])
    print("Marks:\n", marks)
    print("Shape:", marks.shape)
    print("Student averages:", marks.mean(axis=1).round(2))
    print("Subject averages:", marks.mean(axis=0).round(2))
    print("With grace marks:\n", marks + 5)
    print("Weighted scores (original marks):", np.dot(marks, weights).round(2))


def clean_employees():
    source = pd.read_csv(HERE / "employees.csv")
    source.info()
    print(source.describe())
    print("First two rows:\n", source.iloc[:2])
    print("Chennai employees:\n", source.loc[source["city"] == "Chennai", ["name", "salary"]])

    raw = source.copy()
    raw.loc[raw["id"].isin([2, 6]), "salary"] = np.nan
    raw = pd.concat([raw, raw.iloc[[0]]], ignore_index=True)
    raw.to_csv(HERE / "employees_raw.csv", index=False)

    raw = pd.read_csv(HERE / "employees_raw.csv")
    print("Missing salaries:", raw["salary"].isna().sum(), "Duplicate rows:", raw.duplicated().sum())
    clean = raw.drop_duplicates().copy()
    clean = clean.astype({"id": "int64", "name": "string", "city": "string", "department": "string"})
    salary = pd.to_numeric(clean["salary"], errors="raise")
    median = salary.median()
    clean["imputed"] = salary.isna()
    clean["salary"] = salary.fillna(median).astype(float)
    clean.to_csv(HERE / "employees_clean.csv", index=False)
    print(f"Filled {clean['imputed'].sum()} missing salaries with the median of {median:,.0f}.")
    return clean


def department_report(clean):
    departments = pd.DataFrame([
        ("Sales", "Latha", 1800000), ("HR", "Ravi", 1600000),
        ("IT", "Asha", 3200000), ("Finance", "Vijay", 1500000),
        ("Legal", "Uma", 900000),
    ], columns=["department", "head", "budget"])
    departments.to_csv(HERE / "departments.csv", index=False)
    departments = pd.read_csv(HERE / "departments.csv")
    summary = clean.groupby("department", as_index=False).agg(
        headcount=("id", "size"), average_salary=("salary", "mean"),
        maximum_salary=("salary", "max"),
    )
    print("Department statistics:\n", summary.to_string(index=False))
    for how in ("inner", "left", "outer"):
        joined = pd.merge(departments, summary, on="department", how=how,
                          indicator=True, validate="one_to_one")
        joined["headcount"] = joined["headcount"].fillna(0).astype(int)
        print(f"\n{how} join:\n", joined.to_string(index=False))
        if how == "outer":
            empty = joined.loc[joined["_merge"] == "left_only", "department"]
            print("Departments with no employees:", ", ".join(empty))
    return summary


def save_chart(ax, filename, title, xlabel, ylabel):
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.legend()
    ax.figure.tight_layout()
    ax.figure.savefig(HERE / filename, dpi=150)
    plt.close(ax.figure)


def charts(clean, summary):
    pay = clean["salary"] / 1000
    _, ax = plt.subplots()
    ax.bar(summary["department"], summary["average_salary"] / 1000, label="Mean salary")
    save_chart(ax, "bar.png", "Average pay in staffed departments", "Department", "Monthly salary (thousands)")

    _, ax = plt.subplots()
    ax.hist(pay, bins=np.arange(30, 101, 10), edgecolor="white", label="Employees")
    save_chart(ax, "histogram.png", "Distribution of monthly pay", "Monthly salary (thousands)", "Employees")

    _, ax = plt.subplots()
    for imputed, group in clean.groupby("imputed"):
        ax.scatter(group["name"], group["salary"] / 1000, marker="D" if imputed else "o",
                   label="Median-filled" if imputed else "Reported")
    save_chart(ax, "scatter.png", "Reported and median-filled salaries", "Employee", "Monthly salary (thousands)")

    _, ax = plt.subplots()
    cumulative = pay.sort_values(ascending=False).cumsum()
    ranks = np.arange(1, len(pay) + 1)
    ax.plot(ranks, cumulative, marker="o", label="Cumulative payroll")
    ax.set_xticks(ranks)
    save_chart(ax, "line.png", "Payroll from highest earner to lowest", "Number of employees included", "Monthly payroll (thousands)")


if __name__ == "__main__":
    marks_demo()
    employees = clean_employees()
    summary = department_report(employees)
    charts(employees, summary)
    insights = [
        "Bar: Finance has the highest mean monthly salary (90,000), based on one employee.",
        "Histogram: Four of eight salaries fall between 60,000 inclusive and 70,000 exclusive.",
        "Scatter: Priya and Meena share a salary of 64,000 because both values were filled with the median.",
        "Line: The three highest salaries contribute 233,000 of the 499,000 monthly payroll (46.7%).",
    ]
    (HERE / "insights.txt").write_text("\n".join(insights) + "\n", encoding="utf-8")
    print(*insights, sep="\n")
