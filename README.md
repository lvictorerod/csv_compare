# 📊 CSV Column Comparator

A simple and efficient **command-line tool** to compare two CSV files by specific columns, ensuring the values are identical across both files — either by row index or custom key columns. It identifies mismatches and provides options to export the results in CSV or HTML format.
---

## ✅ Features

1. **Compare CSV Files**:
  - Compare two CSV files row by **Row index** or by specified  **Key column(s)** (e.g., `FamilyId`).
  - Case-insensitive and whitespace-trimmed comparison
  - Handles missing columns, rows, and mismatched keys gracefully
  - Supports large files efficiently with `pandas`

2. **Export Mismatches**:
   - Export mismatches to a CSV file using the `--export-mismatches` option.
   - Generate an HTML report with mismatches highlighted using the `--export-html` option.

3. **Ignore Column Order**:
   - Use the `--ignore-column-order` flag to align columns by name, ignoring their order in the files.

4. **Detailed Console Output**:
   - Displays mismatches in the console for quick review.
   - Confirms paths of generated CSV and HTML files.
---

## 🛠 Requirements
- Python 3.x
- pandas library (`pip install pandas`)

🔧 How It Works
- Loads both CSV files as DataFrames with string values.
- Compares each row’s column values by:
  - Exact row index match, or
  - Keyed match using one or more columns.
- Differences are printed with row/key, column name, and differing values.

🚀 Usage
Run the script with the following command:
```bash
python csv_compare.py <file1> <file2> --columns <column1> <column2> ... [options]
```

**Arguments**
- `file1.csv`: Path to the first CSV file.  
- `file2.csv`: Path to the second CSV file.  
- `--columns`: List of columns to compare (**required**).  
- `--keys`: Optional key column(s) to compare by. If omitted, the comparison is done row by row.  
- `--export-mismatches <output.csv>`: Path to export mismatches as a CSV file.  
- `--export-html <output.html>`: Path to export mismatches as an HTML file.  
- `--ignore-column-order`: Ignore column order and align columns by name.
- `--unordered-columns`: Allows the user to specify columns that require order-independent comparison.

1. Basic command
Compare two CSV files by specific columns using row index:
```bash
python csv_compare.py file1.csv file2.csv --columns ColumnA ColumnB
```
2. Using key column(s)
Compare using FamilyId as a unique key:
```bash
python csv_compare.py file1.csv file2.csv --columns ColumnA ColumnB --keys KeyColumn
```
3. Multiple key columns
```bash
python csv_compare.py file1.csv file2.csv --columns ColumnA --keys KeyColumn1 KeyColumn2
```
4. Export Mismatches to CSV
```bash
python csv_compare.py file1.csv file2.csv --columns ColumnA ColumnB --export-mismatches mismatches.csv
```
5. Generate an HTML report with mismatches highlighted:
```bash
python csv_compare.py file1.csv file2.csv --columns ColumnA ColumnB --export-html mismatches.html
```
6. Align columns by name and ignore their order:
```bash
python csv_compare.py file1.csv file2.csv --columns ColumnA ColumnB --ignore-column-order
```
7. Compare with Order-Independent Columns:
```bash
python csv_compare.py file1.csv file2.csv --columns Members Age --unordered-columns Members
```
8. Full Example:
```bash
python csv_compare.py file1.csv file2.csv --columns ColumnA ColumnB --keys KeyColumn --export-mismatches mismatches.csv --export-html mismatches.html --ignore-column-order
```

📄 Example Output
🔍 Comparing by keys: ['KeyColumn']

❗ Found 2 mismatches:

Key ('101',), Column 'Members': File1='23,45,67', File2='23,45'
Key ('102',), Column 'FamilyName': File1='Smith Family', File2='Smiths Family'

✅ If all values match:
🔍 Comparing by keys: ['KeyColumn']
✅ All specified columns match in both files!
