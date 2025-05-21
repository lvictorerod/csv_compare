# 📊 CSV Column Comparator

A simple and efficient **command-line tool** to compare two CSV files by specific columns, ensuring the values are identical across both files — either by row index or custom key columns.

---

## ✅ Features

- Compare two CSV files by:
  - **Row index**
  - **Key column(s)** (e.g., `FamilyId`)
- Case-insensitive and whitespace-trimmed comparison
- Handles missing columns, rows, and mismatched keys gracefully
- Outputs detailed mismatch reports directly to the console
- Supports large files efficiently with `pandas`

---

## 🛠 Requirements

- Python 3.7+
- Dependencies:
  - `pandas`

Install requirements using:
```bash
pip install pandas
```

🔧 How It Works
- Loads both CSV files as DataFrames with string values.
- Compares each row’s column values by:
  - Exact row index match, or
  - Keyed match using one or more columns.
- Differences are printed with row/key, column name, and differing values.

🚀 Usage
1. Basic command
Compare two CSV files by specific columns using row index:
```bash
python csv_compare.py file1.csv file2.csv --columns FamilyId FamilyName MemberCount Members
```

1. Using key column(s)
Compare using FamilyId as a unique key:
```bash
python csv_compare.py file1.csv file2.csv --columns FamilyName MemberCount Members --keys FamilyId
```

1. Multiple key columns
```bash
python csv_compare.py file1.csv file2.csv --columns Value --keys FamilyId MemberId
```

📄 Example Output
🔍 Comparing by keys: ['FamilyId']

❗ Found 2 mismatches:

Key ('101',), Column 'Members': File1='23,45,67', File2='23,45'
Key ('102',), Column 'FamilyName': File1='Smith Family', File2='Smiths Family'

✅ If all values match:
🔍 Comparing by keys: ['FamilyId']
✅ All specified columns match in both files!
