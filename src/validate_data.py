import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def validate(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Run validation checks on cleaned payroll data. Returns (clean_df, report)."""
    report = {
        "total_records": len(df),
        "issues": []
    }

    # 1. Null checks
    nulls = df.isnull().sum()
    null_cols = nulls[nulls > 0]
    if not null_cols.empty:
        for col, count in null_cols.items():
            msg = f"{count} null value(s) in column '{col}'"
            report["issues"].append(msg)
            logger.warning(msg)

    # 2. Negative pay
    neg_gross = df[df["gross_pay"] < 0]
    if not neg_gross.empty:
        msg = f"{len(neg_gross)} records with negative gross_pay"
        report["issues"].append(msg)
        logger.warning(msg)

    neg_net = df[df["net_pay"] < 0]
    if not neg_net.empty:
        msg = f"{len(neg_net)} records with negative net_pay"
        report["issues"].append(msg)
        logger.warning(msg)

    # 3. Zero pay employees
    zero_pay = df[df["gross_pay"] == 0]
    if not zero_pay.empty:
        msg = f"{len(zero_pay)} employees with $0 gross pay"
        report["issues"].append(msg)
        logger.warning(msg)

    # 4. Outlier detection (gross pay > 3 std deviations from mean)
    mean = df["gross_pay"].mean()
    std = df["gross_pay"].std()
    outliers = df[df["gross_pay"] > mean + 3 * std]
    if not outliers.empty:
        msg = f"{len(outliers)} high-pay outliers (>3 std devs above mean)"
        report["issues"].append(msg)
        logger.warning(msg)
        report["outliers"] = outliers[["employee_id", "department", "job_title", "gross_pay"]].to_dict("records")

    # 5. Net pay should be less than gross pay
    invalid_net = df[df["net_pay"] >= df["gross_pay"]]
    if not invalid_net.empty:
        msg = f"{len(invalid_net)} records where net_pay >= gross_pay (tax not applied)"
        report["issues"].append(msg)
        logger.warning(msg)

    # 6. Unknown employment types
    valid_types = {"Full Time", "Part Time"}
    unknown_types = df[~df["employment_type"].isin(valid_types)]
    if not unknown_types.empty:
        msg = f"{len(unknown_types)} records with unknown employment_type"
        report["issues"].append(msg)
        logger.warning(msg)

    # Drop rows with null gross_pay or net_pay (unfixable)
    before = len(df)
    df = df.dropna(subset=["gross_pay", "net_pay"])
    dropped = before - len(df)
    if dropped:
        logger.info(f"Dropped {dropped} rows with null pay values")

    report["valid_records"] = len(df)
    report["passed"] = len(report["issues"]) == 0

    if report["passed"]:
        logger.info("All validation checks passed.")
    else:
        logger.info(f"Validation complete. {len(report['issues'])} issue(s) found.")

    return df, report


if __name__ == "__main__":
    df = pd.read_csv("data/clean_payroll.csv")
    _, report = validate(df)

    print("\n--- Validation Report ---")
    print(f"Total records  : {report['total_records']}")
    print(f"Valid records  : {report['valid_records']}")
    print(f"Issues found   : {len(report['issues'])}")
    for issue in report["issues"]:
        print(f"  ⚠ {issue}")
    print("-------------------------")
