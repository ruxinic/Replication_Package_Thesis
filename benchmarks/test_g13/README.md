# test_g13 - G13 Custom Benchmarks

**G13** encourages developers to "put processes or threads on sleep state if they are waiting for I/O operations or they are no longer active."

Because this guideline targets a very specific behavior (what a process does *while it waits*), it was difficult to find existing published benchmarks that isolate this pattern cleanly; the closest candidates were some "async" benchmarks in PyPerformance, but they were too complex for a clean baseline-optimized comparison. We therefore wrote 5 benchmarks from scratch, each simulating a different type of wait state a Python program can be in.

Each benchmark folder/file pair follows the same structure: a `_baseline` version showing the "naive"/blocking or CPU-wasteful way of waiting, and a `_g13` version showing the guideline-compliant way of waiting (using `asyncio` to suspend execution instead of blocking or spinning).

## Benchmarks overview

| # | File prefix | Scenario | What it tests |
|---|---|---|---|
| b1 | `sleep_` | CPU sleep block | A program waiting a fixed duration for an external resource to respond |
| b2 | `polling_` | Continuous socket polling | A program waiting for data to arrive on a socket |
| b3 | `cws_` | Concurrent I/O tasks | A program firing off several independent I/O-bound tasks at once |
| b4 | `flag_` | External condition / state flag | A program waiting for an external condition or flag to change |
| b5 | `disk_` | Disk I/O | A program waiting on physical storage to read/write data |

## b1 - Sleep blocks the CPU (`sleep_baseline.py` / `sleep_g13.py`)

Simulates a program that needs to wait a fixed amount of time for an external resource to become available.

- **Baseline**: uses `time.sleep()`, a synchronous blocking call. The thread stays registered as "active" with the OS scheduler even though it does nothing productive during the wait.
- **G13**: uses `await asyncio.sleep()` inside an event loop, explicitly signaling that the coroutine is waiting on a timer and can be suspended, freeing the CPU to enter a low-power state.

## b2 - Continuous polling from a socket (`polling_baseline.py` / `polling_g13.py`)

A classic I/O anti-pattern: repeatedly checking if data has arrived on a socket instead of waiting for a notification.

- **Baseline**: a non-blocking socket in a tight `while True` loop, catching `BlockingIOError` and immediately retrying — this pins the CPU core at 100% while nothing has actually happened yet.
- **G13**: replaces the socket-polling loop with `asyncio`, so the process registers its intent to read with the OS and truly suspends (0% CPU) until the kernel signals that data is available.

## b3 - Concurrent I/O tasks (`cws_baseline.py` / `cws_g13.py`)

Simulates an application firing off several independent I/O-bound tasks at the same time (e.g. pulling data from multiple API endpoints or running several queries concurrently). "CWS" stands for concurrent-waits.

- **Baseline**: each worker blocks the thread sequentially with `time.sleep()`, so a second worker cannot even begin waiting until the first one is completely done, the wait times stack up.
- **G13**: uses `asyncio.gather()` to launch all workers' wait states at (almost) the same moment, so the single execution thread registers all wake-up callbacks with the kernel and handles the downtime in one overlapped batch instead of sequentially.

## b4 - External condition / state flag (`flag_baseline.py` / `flag_g13.py`)

Simulates a long-running process waiting for an external condition or state flag to change (e.g. waiting for a background computation to finish or a hardware status flag to flip). This highlights the classic **active vs. passive waiting** problem:

- **Baseline**: an empty `while` loop (a busy-wait / spin lock) continuously checks the flag as fast as possible. Execution time looks clean (~2 seconds total), but the core runs at 100% the entire time, since it is not actually doing anything but checking.
- **G13**: adds `await asyncio.sleep(0.005)` inside the check loop, so between checks the coroutine yields the CPU and lets it drop to a low-power state. Total wall-clock time stays roughly the same, but average power draw collapses toward idle.

## b5 - Disk-bound file I/O (`disk_baseline.py` / `disk_g13.py`)

Simulates a program writing and reading a file, which is traditionally a blocking operation, since it requires waiting on the physical storage controller.

- **Baseline**: uses a standard synchronous `open()`/`write()`/`read()` sequence. While the disk controller is busy, the entire application thread freezes until the OS returns a success flag.
- **G13**: offloads the blocking file operations to a separate thread via `asyncio.to_thread()`, so the main event loop stays free while a background thread absorbs the disk wait.
