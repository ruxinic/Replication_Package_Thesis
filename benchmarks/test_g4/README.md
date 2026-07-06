# test_g4 - G4 Custom Benchmarks

**G4** encourages developers to "use short-circuit versions of logical operators where the second argument of a logical expression is evaluated only if the first argument is insufficient to determine the value of the expression."

Finding published benchmarks that actually exercise this pattern in a measurable way turned out to be difficult. We first tried adapting a handful of existing benchmarks with minimal changes such as swapping `and`/`or` for their non-short-circuiting bitwise equivalents `&`/`|` to create an "unoptimized" baseline. We also wrote one benchmark entirely from scratch (`network`), and repurposed two Rosetta Code snippets by deliberately "un-optimizing" them into an eager-evaluation baseline (`log_processing`, `short_circ_eval`).

Each benchmark folder/file pair follows the same structure: an unoptimized `_baseline`, and a `_g4` optimized version.

## Benchmarks overview

| File prefix | Benchmark | Origin | What it tests |
|---|---|---|---|
| `network_` | Network Packet Routing | Written from scratch | Deeply nested `if` checks vs. flattened short-circuit condition |
| `lp_` | Log Processing | Adapted from Rosetta Code, un-optimized into baseline | Nested `if` checks vs. short-circuit condition when filtering log rows |
| `sc_` | Short Circuit Evaluation | Adapted from Rosetta Code, un-optimized into baseline | Eager bitwise (`&`, `\|`) vs. short-circuit (`and`, `or`) logical operators |

## network - Network Packet Routing (`network_baseline.py` / `network_g4.py`)

Simulates a high-traffic network router that must validate every incoming packet for structural integrity before allowing it through, e.g. checking that the packet exists, has a non-zero payload, and does not come from a blacklisted zone (`0.0.0.0`). A packet that passes all checks then undergoes an expensive simulated checksum calculation.

- **Baseline**: uses deeply nested `if` statements — `packet is not None`, then `payload_len > 0`, then `ip != "0.0.0.0"`, each check indented inside the previous one. Because of how the checks are structured, all of the cheap validations still run in sequence before the expensive checksum step, mirroring how many real-world routers are naively written.
- **G4**: flattens the same checks into a single boolean expression chained with `and`. If an early condition fails (e.g. the packet is `None` or already dropped), the interpreter never evaluates the expensive checksum computation `(payload_len ** 7) % 9999991` at all.

## lp - Log Processing (`lp_baseline.py` / `lp_g4.py`)

Simulates filtering a large stream of log rows (50,000,000 entries, a mix of valid logs, `None` values, and empty strings) to find critical error entries from a specific IP range.

- **Baseline**: nested `if` statements check `row is not None`, then `len(row) > 0`, then `row.startswith("192.")`, then `"500" in row`, each nested inside the previous check.
- **G4**: flattens the same four conditions into a single `and`-chained expression, so as soon as one condition fails (e.g. the row is `None` or empty), the remaining, more expensive string checks are skipped.

## sc - Short Circuit Evaluation (`sc_baseline.py` / `sc_g4.py`)

A minimal, direct test of short-circuit evaluation itself, based on the classic Rosetta Code short-circuit-evaluation example, run for 50,000,000 iterations over all four boolean combinations of two dummy functions `a()` and `b()`.

- **Baseline**: replaces the logical `and`/`or` operators with their eager, non-short-circuiting bitwise equivalents `&` and `|`, forcing both `a(i)` and `b(j)` to be evaluated in full every time, regardless of the outcome of the first.
- **G4**: restores the original Rosetta Code logic, using `and`/`or`, so `b(j)` is skipped whenever `a(i)` alone is already sufficient to determine the result.

## Note on `lp` and `sc`

Both `lp` (log processing) and `sc` (short-circuit evaluation) originate from Rosetta Code. Since the original snippets already used short-circuit evaluation (the pattern G4 recommends), we could not use them as-is for a fair before/after comparison, so the "baseline" versions in this folder are our deliberately unoptimized rewrites of the original code, and the `_g4` versions restore the original short-circuit logic.
