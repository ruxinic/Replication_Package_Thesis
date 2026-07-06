import sys

def generate_mock_data():
    # Generates 2,000,000 log rows (Mix of valid logs, None types, and empty strings)
    print("Generating dataset...", flush=True)
    logs = []
    for i in range(50_000_000):
        if i % 4 == 0:
            logs.append("192.168.1.10 - CRITICAL - 500 Internal Error")
        elif i % 4 == 1:
            logs.append(None)
        elif i % 4 == 2:
            logs.append("")
        else:
            logs.append("10.0.0.5 - INFO - 200 OK")
    return logs

def run_g4(logs):
    matched_count = 0
    # G4: flatten if conditions
    for row in logs:
        if row is not None and len(row) > 0 and row.startswith("192.") and "500" in row:
            matched_count += 1                        
    return matched_count

if __name__ == "__main__":
    dataset = generate_mock_data()
    matches = run_g4(dataset)
    print(f"\n Matches: {matches:,}")