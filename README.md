# Python Assessment

## Overview

This repository contains my Python Assessment focused on understanding pandas behavior and identifying issues that may produce incorrect results without causing code execution failures.

The assessment covers practical pandas concepts, debugging, data validation, and defensive programming techniques.

## Topics Covered

* Views vs Copies in pandas
* Chained assignment and `SettingWithCopy` warnings
* Copy-on-Write behavior
* `inplace=True` on column selections
* Merge cardinality and duplicate keys
* `validate` parameter in `pd.merge()`
* `groupby()` and missing values
* `NaN` comparison semantics
* `Series.equals()`
* Division by zero and `inf` / `NaN`
* Text standardization
* DataFrame validation and defensive checks
* Missing values and distinct-value analysis

## Assessment Structure

### Section A — Predict the Output

* **Q1:** Views vs Copies / Chained Assignment
* **Q2:** Merge Cardinality
* **Q3:** `groupby()` and NaN
* **Q4:** `inplace=True` on Column Selection
* **Q5:** NaN Comparison Semantics

### Section B — Write the Code

* **Q6:** Standardizing Text Values
* **Q7:** Diagnosing a Merge Producing Too Many Rows
* **Q8:** DataFrame Summary Function

### Section C — Debugging

* **Q9:** Profit Margin and Division by Zero
* **Q10:** Diagnosing Incorrect Regional Totals

## Key Defensive Checks

The assessment demonstrates the importance of checking:

```python
df.shape
df.nunique()
df.isna().sum()
df.duplicated().sum()
```

These checks help identify unexpected row counts, duplicate records, missing values, and data-quality issues before performing analysis.

## Files

```text
Python-Assessment/
│
├── Python Assessment/
│  └── python_assessment.py
│  
│
└── README.md
```

## Technologies Used

* Python
* Pandas
* NumPy

## Purpose

The purpose of this assessment is to develop a better understanding of pandas behavior and to practice writing reliable, defensive data-processing code that can identify silent data issues before they affect analysis.

## Author
Manjunath Kumbar

