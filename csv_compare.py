import argparse
import pandas as pd
import sys

def load_csv(path):
    """Load a CSV file into a pandas DataFrame."""
    try:
        print(f"📂 Loading file: {path}")
        return pd.read_csv(path, dtype=str).fillna("").applymap(str.strip)
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
                    "Row": i,
                    "Column": col,
                    "File1": row1.get(col, ""),
                    "File2": row2.get(col, "")
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
                    "Key": key if isinstance(key, tuple) else (key,),
                    "Column": col,
                    "File1": row1[col] if row1 is not None and col in row1 else "<missing>",
                    "File2": row2[col] if row2 is not None and col in row2 else "<missing>"
                })
    return mismatches

def print_mismatches(mismatches):
    """Print mismatches in a readable format."""
    if mismatches:
        print(f"\n❗ Found {len(mismatches)} mismatches:\n")
        for m in mismatches:
            if 'Row' in m:
                print(f"Row {m['Row']}, Column '{m['Column']}': File1='{m['File1']}', File2='{m['File2']}'")
            else:
                print(f"Key {m['Key']}, Column '{m['Column']}': File1='{m['File1']}', File2='{m['File2']}'")
    else:
        print("✅ All specified columns match in both files!")

def main():
    parser = argparse.ArgumentParser(description="Compare two CSV files by columns and keys.")
    parser.add_argument("file1", help="Path to first CSV")
    parser.add_argument("file2", help="Path to second CSV")
    parser.add_argument("--columns", nargs="+", required=True, help="Columns to compare")
    parser.add_argument("--keys", nargs="*", help="Optional key column(s). If omitted, compares by row index.")

    args = parser.parse_args()

    # Load CSV files
    df1 = load_csv(args.file1)
    df2 = load_csv(args.file2)

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

if __name__ == "__main__":
    main()