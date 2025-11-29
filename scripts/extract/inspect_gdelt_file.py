# scripts/extract/inspect_gdelt_file.py

from pathlib import Path
import csv

import pandas as pd

# Figure out repo root (scripts/extract -> scripts -> root)
BASE_DIR = Path(__file__).resolve().parents[2]
raw_path = BASE_DIR / "data" / "raw" / "gdelt" / "sample_events.csv"

print("=== GDELT FILE INSPECTION ===")
print(f"File path: {raw_path}")

if not raw_path.exists():
    raise FileNotFoundError(f"File not found at {raw_path}")

# 1) Show first 5 raw lines (no parsing yet)
print("\n--- First 5 raw lines ---")
with open(raw_path, "r", encoding="latin1") as f:
    first_lines = []
    for i in range(5):
        try:
            line = next(f)
        except StopIteration:
            break
        first_lines.append(line)

for i, line in enumerate(first_lines, start=1):
    print(f"{i}: {line.rstrip()}")

# 2) Try to detect delimiter
print("\n--- Delimiter detection ---")
sample_text = "".join(first_lines)

try:
    dialect = csv.Sniffer().sniff(sample_text)
    delim = dialect.delimiter
    print("Detected delimiter (repr):", repr(delim))
except Exception as e:
    print("Could not sniff delimiter:", e)
    delim = ","  # fallback

# 3) Try reading a small chunk with pandas using that delimiter
print("\n--- Pandas preview ---")
try:
    df = pd.read_csv(
        raw_path,
        encoding="latin1",
        engine="python",
        sep=delim,
        header=None,          # treat as no header for now
        on_bad_lines="skip",
        nrows=5               # only first 5 rows
    )
    print("Shape (first 5 rows):", df.shape)
    print(df.head())
except Exception as e:
    print("Error reading with pandas:", e)

print("\n=== END INSPECTION ===")
