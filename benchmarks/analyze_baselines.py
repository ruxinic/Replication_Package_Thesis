"""
In the local environment we have created a separate folder which contains all used baselines. 
This file, alongside baselines_metrics.py, are in said folder.
Runs radon (LOC + cyclomatic complexity) and pylint (quality score)
over every .py file in the folder, and writes a combined CSV file.

Usage:
    pip install radon pylint --break-system-packages
    python analyze_baselines.py

Output:
    baselines_metrics.csv  (in the current directory)
"""

import subprocess
import sys
import os
import csv
import re
import json


def get_loc(filepath):
    """Run `radon raw` and extract LOC / LLOC / SLOC / comments / blank."""
    result = subprocess.run(
        ["radon", "raw", "-j", filepath],
        capture_output=True, text=True
    )
    try:
        data = json.loads(result.stdout)
        stats = data[filepath]
        return stats["loc"], stats["lloc"], stats["sloc"], stats["comments"], stats["blank"]
    except Exception:
        return None, None, None, None, None


def get_complexity(filepath):
    """Run `radon cc` and compute the average cyclomatic complexity across functions."""
    result = subprocess.run(
        ["radon", "cc", "-j", filepath],
        capture_output=True, text=True
    )
    try:
        data = json.loads(result.stdout)
        blocks = data.get(filepath, [])
        if not blocks:
            return 0, 0
        complexities = [b["complexity"] for b in blocks]
        avg_cc = sum(complexities) / len(complexities)
        max_cc = max(complexities)
        return round(avg_cc, 2), max_cc
    except Exception:
        return None, None


def get_pylint_score(filepath):
    """Run pylint and extract the overall score out of 10."""
    result = subprocess.run(
        ["pylint", filepath, "--score=y"],
        capture_output=True, text=True
    )
    match = re.search(r"rated at ([\-0-9\.]+)/10", result.stdout)
    if match:
        return float(match.group(1))
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_benchmarks.py /path/to/baselines")
        sys.exit(1)

    folder = sys.argv[1]
    py_files = []
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(".py"):
                py_files.append(os.path.join(root, f))

    py_files.sort()
    print(f"Found {len(py_files)} Python files.\n")

    rows = []
    for filepath in py_files:
        name = os.path.basename(filepath)
        print(f"Analyzing {name} ...")

        loc, lloc, sloc, comments, blank = get_loc(filepath)
        avg_cc, max_cc = get_complexity(filepath)
        pylint_score = get_pylint_score(filepath)

        rows.append({
            "benchmark": name,
            "loc": loc,
            "lloc": lloc,
            "sloc": sloc,
            "comments": comments,
            "blank": blank,
            "avg_cyclomatic_complexity": avg_cc,
            "max_cyclomatic_complexity": max_cc,
            "pylint_score": pylint_score,
        })

    out_path = "benchmark_metrics.csv"
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDone. Results written to {out_path}")

    print("\n--- Summary ---")
    for r in rows:
        print(f"{r['benchmark']:35s} LOC={r['loc']:>5} "
              f"avgCC={r['avg_cyclomatic_complexity']:>6} "
              f"pylint={r['pylint_score']}")


if __name__ == "__main__":
    main()
