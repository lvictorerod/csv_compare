import argparse
import pandas as pd
import sys

def load_csv(path):
    """Load a CSV file into a pandas DataFrame."""
    try:
        print(f"📂 Loading file: {path}")
        return pd.read_csv(path, dtype=str).fillna("").map(str.strip)
    except Exception as e:
        print(f"❌ Error loading {path}: {e}")
        sys.exit(1)

def validate_columns(df, columns, file_name):
    """Validate that the required columns exist in the DataFrame."""
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        print(f"❌ Missing columns in {file_name}: {missing_columns}")
        sys.exit(1)

def compare_by_index(df1, df2, columns):
    """Compare two DataFrames row by row based on the specified columns."""
    mismatches = []
    min_len = min(len(df1), len(df2))
    for i in range(min_len):
        row1, row2 = df1.iloc[i], df2.iloc[i]
        for col in columns:
            val1 = str(row1.get(col, "")).strip().lower()
            val2 = str(row2.get(col, "")).strip().lower()
            if val1 != val2:
                mismatches.append({
                    "KeyOrRow": i,  # Use 'KeyOrRow' instead of 'Row'
                    "ColumnName": col,
                    "File1Value": row1.get(col, ""),
                    "File2Value": row2.get(col, "")
                })
    return mismatches

def compare_by_key(df1, df2, key_columns, compare_columns):
    """Compare two DataFrames based on key columns and specified comparison columns."""
    df1 = df1.set_index(key_columns)
    df2 = df2.set_index(key_columns)

    mismatches = []
    all_keys = df1.index.union(df2.index)

    for key in all_keys:
        row1 = df1.loc[key] if key in df1.index else None
        row2 = df2.loc[key] if key in df2.index else None
        for col in compare_columns:
            val1 = str(row1[col]).strip().lower() if row1 is not None and col in row1 else "<missing>"
            val2 = str(row2[col]).strip().lower() if row2 is not None and col in row2 else "<missing>"
            if val1 != val2:
                mismatches.append({
                    "KeyOrRow": key if isinstance(key, tuple) else (key,),  # Use 'KeyOrRow' instead of 'Key'
                    "ColumnName": col,
                    "File1Value": row1[col] if row1 is not None and col in row1 else "<missing>",
                    "File2Value": row2[col] if row2 is not None and col in row2 else "<missing>"
                })
    return mismatches

def print_mismatches(mismatches):
    """Print mismatches in a readable format."""
    if mismatches:
        print(f"\n❗ Found {len(mismatches)} mismatches:\n")
        for m in mismatches:
            key_or_row = m['KeyOrRow']
            column = m['ColumnName']
            file1_value = m['File1Value']
            file2_value = m['File2Value']
            print(f"Key/Row {key_or_row}, Column '{column}': File1='{file1_value}', File2='{file2_value}'")
    else:
        print("✅ All specified columns match in both files!")

def export_mismatches_to_csv(mismatches, output_path):
    """Export mismatches to a CSV file."""
    df = pd.DataFrame(mismatches)
    df.to_csv(output_path, index=False)
    print(f"📄 Mismatches exported to CSV: {output_path}")

def export_mismatches_to_html(mismatches, output_path):
    """Export mismatches to an HTML file."""
    html_content = "<html><head><style>"
    html_content += "table {border-collapse: collapse; width: 100%;}"
    html_content += "th, td {border: 1px solid black; padding: 8px; text-align: left;}"
    html_content += "td.diff {background-color: #f8d7da;}"
    html_content += "</style></head><body>"
    html_content += f"<h1>Mismatches Report</h1>"
    html_content += f"<p>Total mismatches: {len(mismatches)}</p>"
    html_content += "<table><tr><th>Key/Row</th><th>Column</th><th>File1</th><th>File2</th></tr>"

    for m in mismatches:
        key_or_row = m['KeyOrRow']
        column = m['ColumnName']
        file1_value = m['File1Value']
        file2_value = m['File2Value']
        html_content += f"<tr><td>{key_or_row}</td><td>{column}</td>"
        html_content += f"<td class='diff'>{file1_value}</td><td class='diff'>{file2_value}</td></tr>"

    html_content += "</table></body></html>"

    with open(output_path, "w") as f:
        f.write(html_content)
    print(f"📄 Mismatches exported to HTML: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Compare two CSV files by columns and keys.")
    parser.add_argument("file1", help="Path to first CSV")
    parser.add_argument("file2", help="Path to second CSV")
    parser.add_argument("--columns", nargs="+", required=True, help="Columns to compare")
    parser.add_argument("--keys", nargs="*", help="Optional key column(s). If omitted, compares by row index.")
    parser.add_argument("--export-mismatches", help="Path to export mismatches as a CSV file")
    parser.add_argument("--export-html", help="Path to export mismatches as an HTML file")
    parser.add_argument("--ignore-column-order", action="store_true", help="Ignore column order and align columns by name")

    args = parser.parse_args()

    # Load CSV files
    df1 = load_csv(args.file1)
    df2 = load_csv(args.file2)

     # Handle column order
    if args.ignore_column_order:
        common_columns = list(set(df1.columns).intersection(set(df2.columns)))
        df1 = df1[common_columns]
        df2 = df2[common_columns]
        print(f"🔄 Ignoring column order. Using common columns: {common_columns}")

    # Validate columns
    validate_columns(df1, args.columns, args.file1)
    validate_columns(df2, args.columns, args.file2)
    if args.keys:
        validate_columns(df1, args.keys, args.file1)
        validate_columns(df2, args.keys, args.file2)

    # Perform comparison
    if args.keys:
        print(f"🔍 Comparing by keys: {args.keys}")
        mismatches = compare_by_key(df1, df2, args.keys, args.columns)
    else:
        print(f"🔍 Comparing by row index")
        mismatches = compare_by_index(df1, df2, args.columns)

    # Print mismatches
    print_mismatches(mismatches)

     # Export mismatches
    if args.export_mismatches:
        export_mismatches_to_csv(mismatches, args.export_mismatches)
    if args.export_html:
        export_mismatches_to_html(mismatches, args.export_html)

if __name__ == "__main__":
    main()