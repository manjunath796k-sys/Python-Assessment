# ============================================================
# PYTHON ASSESSMENT
# ============================================================

import pandas as pd
import numpy as np


# ============================================================
# SECTION A — PREDICT THE OUTPUT
# ============================================================


# ------------------------------------------------------------
# Q1 — Views vs Copies / Chained Assignment
# ------------------------------------------------------------

# Prediction:
# The original df is expected to remain unchanged, so the output
# should be [10, 20, 30].
#
# The assignment sub['b'] = 0 is being performed on the sliced
# DataFrame `sub`, not reliably on the original df.
#
# Depending on the pandas version and Copy-on-Write settings,
# pandas may raise a SettingWithCopyWarning or a related
# ChainedAssignmentError warning.
#
# The warning tells us that we should not rely on modifying a
# DataFrame obtained through a slice. We should use .loc on the
# original DataFrame when we intend to modify it.

df = pd.DataFrame({'a': [1, 2, 3], 'b': [10, 20, 30]})

sub = df[df['a'] > 1]

sub['b'] = 0

print("Q1 Output:", df['b'].tolist())


# Correct defensive approach if we WANT to modify df:
# df.loc[df['a'] > 1, 'b'] = 0


# ============================================================
# Q2 — Merge Cardinality
# ============================================================

# Prediction:
# The merge returns 5 rows.
#
# For k=1:
# left has 2 rows and right has 2 rows.
# Therefore: 2 x 2 = 4 combinations.
#
# For k=2:
# left has 1 row and right has 1 row.
# Therefore: 1 x 1 = 1 combination.
#
# Total = 4 + 1 = 5 rows.
#
# This demonstrates that merging on a non-unique key can multiply
# rows. This is a many-to-many relationship for key k.

left = pd.DataFrame({
    'k': [1, 1, 2],
    'v': ['a', 'b', 'c']
})

right = pd.DataFrame({
    'k': [1, 1, 2],
    'w': ['x', 'y', 'z']
})

print("Q2 Output:", len(left.merge(right, on='k')))


# Defensive merge:
# Use validate='one_to-one', 'one_to_many', or 'many_to_one'
# when the expected relationship is known.


# ============================================================
# Q3 — groupby() and NaN
# ============================================================

# Prediction:
# By default, groupby(dropna=True) excludes the None/NaN group.
#
# Therefore the row where g is None is not included.
#
# Expected output:
# {'a': 5, 'b': 2}
#
# To include the missing group, use:
# d.groupby('g', dropna=False)['v'].sum()
#
# This is useful when missing values themselves are meaningful,
# or when we need to account for every row during reporting.

d = pd.DataFrame({
    'g': ['a', 'b', None, 'a'],
    'v': [1, 2, 3, 4]
})

print("Q3 Output:", d.groupby('g')['v'].sum().to_dict())


# ============================================================
# Q4 — inplace=True on Column Selection
# ============================================================

# Prediction:
# Under pandas Copy-on-Write behaviour, using inplace=True on
# df['x'].fillna(...) is not a safe way to modify the original
# DataFrame.
#
# The missing value may remain, producing:
# 1
#
# The correct approach is to assign the result back:
# df['x'] = df['x'].fillna(0)
#
# This avoids chained assignment and works reliably.

df = pd.DataFrame({
    'x': [1, np.nan, 3]
})

df['x'].fillna(0, inplace=True)

print("Q4 Output:", df['x'].isna().sum())


# Correct version:
df = pd.DataFrame({
    'x': [1, np.nan, 3]
})

df['x'] = df['x'].fillna(0)

print("Q4 Correct Output:", df['x'].isna().sum())


# ============================================================
# Q5 — NaN Comparison Semantics
# ============================================================

# Prediction:
#
# (a == b).all()
# returns False.
#
# a.equals(b)
# returns True.
#
# NaN is not equal to NaN using normal == comparison.
#
# However, Series.equals() treats NaN values in the same
# corresponding positions as equal.
#
# For checking whether two pandas datasets/Series match,
# .equals() is generally more appropriate because it checks
# the values and considers corresponding missing values equal.

a = pd.Series([1, np.nan])
b = pd.Series([1, np.nan])

print("Q5 == Output:", (a == b).all())
print("Q5 equals() Output:", a.equals(b))


# ============================================================
# SECTION B — WRITE THE CODE
# ============================================================


# ------------------------------------------------------------
# Q6 — Standardising Text Values
# ------------------------------------------------------------

# Example values:
# "Net banking"
# "NetBanking"
# " netbanking "
#
# .str.strip().str.title() alone is NOT sufficient because:
#
# "Net banking" -> "Net Banking"
# "NetBanking"  -> "Netbanking"
#
# These are still different values.
#
# Therefore, we need an explicit mapping after normalising case
# and whitespace.

df = pd.DataFrame({
    'payment_method': [
        'Net banking',
        'NetBanking',
        ' netbanking ',
        'UPI',
        ' upi '
    ]
})

df['payment_method'] = (
    df['payment_method']
    .str.strip()
    .str.lower()
    .replace({
        'net banking': 'Net Banking',
        'netbanking': 'Net Banking',
        'upi': 'UPI'
    })
)

print("\nQ6 Standardised values:")
print(df['payment_method'].tolist())


# ============================================================
# Q7 — Diagnose a Merge Producing Too Many Rows
# ============================================================

# When a merge produces more rows than either input, the first
# thing to investigate is duplicate keys.
#
# Duplicate keys can create a many-to-many merge.
#
# For example:
# left key appears twice
# right key appears three times
#
# The merge can create 2 x 3 = 6 rows for that key.

left = pd.DataFrame({
    'CustomerID': [1, 1, 2],
    'Sales': [100, 200, 300]
})

right = pd.DataFrame({
    'CustomerID': [1, 1, 1, 2],
    'Region': ['South', 'South', 'North', 'East']
})

# 1. Check input shapes
print("\nQ7 Left shape:", left.shape)
print("Q7 Right shape:", right.shape)

# 2. Check number of unique keys
print("Q7 Left unique keys:", left['CustomerID'].nunique())
print("Q7 Right unique keys:", right['CustomerID'].nunique())

# 3. Check duplicate keys
print(
    "Q7 Left duplicate keys:",
    left['CustomerID'].duplicated().sum()
)

print(
    "Q7 Right duplicate keys:",
    right['CustomerID'].duplicated().sum()
)

# 4. Show the actual duplicated key values
print("\nQ7 Left duplicated keys:")
print(left[left['CustomerID'].duplicated(keep=False)])

print("\nQ7 Right duplicated keys:")
print(right[right['CustomerID'].duplicated(keep=False)])

# 5. Check merge cardinality explicitly
#
# If we expect CustomerID to be unique in right:
#
# result = left.merge(
#     right,
#     on='CustomerID',
#     validate='many_to_one'
# )
#
# If the relationship is violated, pandas raises an error
# instead of silently producing an inflated result.


# ============================================================
# Q8 — DataFrame Summary Function
# ============================================================

def column_summary(df, columns):
    """
    Return a summary for the requested columns.

    For each column, return:
    - missing values
    - number of distinct values
    - data type

    If a requested column does not exist, record the error
    instead of crashing the function.
    """

    summary = []

    for column in columns:

        if column not in df.columns:
            summary.append({
                'column': column,
                'missing_values': None,
                'distinct_values': None,
                'dtype': 'COLUMN NOT FOUND'
            })
            continue

        summary.append({
            'column': column,
            'missing_values': df[column].isna().sum(),
            'distinct_values': df[column].nunique(),
            'dtype': str(df[column].dtype)
        })

    return pd.DataFrame(summary)


# Example for Q8
test_df = pd.DataFrame({
    'name': ['A', 'B', 'A', None],
    'age': [20, 25, np.nan, 30],
    'city': ['Bengaluru', 'Mysuru', 'Bengaluru', 'Mangaluru']
})

print("\nQ8 Summary:")
print(
    column_summary(
        test_df,
        ['name', 'age', 'city', 'salary']
    )
)


# ============================================================
# SECTION C — DEBUGGING
# ============================================================


# ------------------------------------------------------------
# Q9 — Profit Margin and Division by Zero
# ------------------------------------------------------------

# Problem:
#
# The original function performs:
#
# profit / sales * 100
#
# If sales is 0, pandas can produce inf when profit is non-zero.
#
# If both profit and sales are 0, the calculation can produce NaN
# because 0 / 0 is undefined.
#
# Therefore, we should explicitly protect against sales == 0.
#
# A safe approach is to replace zero sales with NaN before division.
# This produces NaN rather than inf for undefined margins.

def margin(df):
    df = df.copy()

    df['margin'] = (
        df['profit']
        .div(df['sales'].replace(0, np.nan))
        .mul(100)
    )

    return df


# Example for Q9
profit_df = pd.DataFrame({
    'profit': [100, 50, 0, -20],
    'sales': [1000, 0, 0, 100]
})

safe_margin_df = margin(profit_df)

print("\nQ9 Safe Margin:")
print(safe_margin_df)

# Optional defensive check:
print("\nQ9 Infinite values:", np.isinf(safe_margin_df['margin']).sum())
print("Q9 Missing margins:", safe_margin_df['margin'].isna().sum())


# ============================================================
# Q10 — Regional Totals Are Wrong
# ============================================================

# Three checks I would run first, in this order:
#
# 1. Check shape and duplicates
#    This rules out duplicate rows or accidental row multiplication
#    during cleaning/merging.
#
# 2. Check missing/invalid Region values
#    This rules out records being excluded from regional groupby
#    results because Region is NaN or inconsistently populated.
#
# 3. Check merge keys and merge cardinality
#    This rules out a bad join that duplicated transactions or
#    assigned records to the wrong region.
#
# These checks should be done before changing the regional totals
# manually.


# Q10 Example defensive checks

# Check 1 — shape and duplicate rows
print("\nQ10 Check 1 — Shape and duplicates")
print("Shape:", safe_margin_df.shape)
print("Duplicate rows:", safe_margin_df.duplicated().sum())


# Check 2 — missing Region values
regional_df = pd.DataFrame({
    'Region': ['South', 'North', 'South', None],
    'Sales': [100, 200, 150, 300]
})

print("\nQ10 Check 2 — Missing Region")
print(regional_df['Region'].isna().sum())
print(regional_df['Region'].value_counts(dropna=False))


# Check 3 — Merge key uniqueness/cardinality
customers = pd.DataFrame({
    'CustomerID': [1, 2, 3],
    'Region': ['South', 'North', 'East']
})

orders = pd.DataFrame({
    'CustomerID': [1, 2, 3, 1],
    'Sales': [100, 200, 300, 150]
})

print("\nQ10 Check 3 — Merge key checks")
print(
    "Customer duplicate keys:",
    customers['CustomerID'].duplicated().sum()
)

print(
    "Order duplicate keys:",
    orders['CustomerID'].duplicated().sum()
)

# Since CustomerID should be unique in customers and can repeat
# in orders, the expected relationship is many-to-one.
merged = orders.merge(
    customers,
    on='CustomerID',
    how='left',
    validate='many_to_one'
)

print("Merged shape:", merged.shape)


# ============================================================
# FINAL DEFENSIVE CHECKS
# ============================================================

# Useful checks before trusting a pandas dataset:
#
# .shape
# .nunique()
# .isna().sum()
# .duplicated().sum()
#
# These checks help identify unexpected row counts, duplicate keys,
# missing data, and unexpected cardinality before analysis.

print("\nFinal defensive checks completed.")