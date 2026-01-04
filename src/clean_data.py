import pandas as pd

df = pd.read_csv("data/data.csv")

# Drop empty unnamed columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Clean currency columns
currency_cols = [
    "Hourly or Event Rate",
    "Projected Annual Salary",
    "Q1 Payments",
    "Q2 Payments",
    "Q3 Payments"
]

for col in currency_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .replace("nan", None)
        .astype(float)
    )

# Create gross pay from quarterly payments
df["gross_pay"] = df[["Q1 Payments", "Q2 Payments", "Q3 Payments"]].sum(axis=1)

# Simulate tax deduction (20%)
df["tax_deduction"] = df["gross_pay"] * 0.20
df["net_pay"] = df["gross_pay"] - df["tax_deduction"]

# Select final columns
clean_df = df[[
    "Record Number",
    "Department Title",
    "Job Class Title",
    "Employment Type",
    "gross_pay",
    "tax_deduction",
    "net_pay"
]]

clean_df.columns = [
    "employee_id",
    "department",
    "job_title",
    "employment_type",
    "gross_pay",
    "tax_deduction",
    "net_pay"
]

clean_df.to_csv("data/clean_payroll.csv", index=False)

print("Payroll data cleaned and saved.")
