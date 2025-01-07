# Table Ops

A collection of simple command-line table manipulation tools written in Python. These tools are designed to be efficient and easy to use for common table operations.

## Tools

### `table-union`

Merges multiple tabular data files (e.g., CSV, TSV) either by unioning rows with identical columns or by performing a join based on shared key columns.

**Key Features:**

*   **Union Mode (Default):** Combines rows from all input files, assuming they have the same columns. Duplicate rows are retained.
*   **Join Mode (`--no-union` or similar):** Performs a join operation based on automatically detected shared key columns. It intelligently identifies potential key columns by looking for columns with unique, non-null values across all input files. This mode merges rows based on matching key values.
*   **Automatic Key Detection:** Automatically identifies suitable columns for joining based on uniqueness and non-null constraints.
*   **Handles various delimiters:** Supports tab-separated (TSV) and comma-separated (CSV) files.
*   **Memory Efficient:** Optimized to handle large files without loading them entirely into memory (where possible).

**Usage Example:**

```bash
table-union file1.tsv file2.tsv file3.tsv > output.tsv
```

```bash
table-summarize data.tsv
```

```bash
table-sort -k Age -k Name data.tsv > sorted_data.tsv
```

**Run Unit Tests:**

```bash
python -m unittest test_table_ops.py
```