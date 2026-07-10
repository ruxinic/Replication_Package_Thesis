# Execution Scripts

This folder contains the scripts used to run the benchmarks on the remote servers and collect energy/time measurements via EnergiBridge.

Both scripts follow the same overall procedure:

1. Reset and recreate the results folder for the benchmark being tested.
2. Build a task list by repeating each script in the `scripts` array 30 times (30 runs per version, as required by the experiment design).
3. Randomize the task list with `shuf` to avoid ordering effects.
4. Execute each run through EnergiBridge, saving the output to an individual `run_N.csv` file, with a 30-second cool-down between runs to reduce thermal throttling.
5. Clean up the temporary task list once all runs are complete.

There are two versions of the script, used on the two different remote servers:

- **Standard version (GL1 server)** - 152 codes executed. Runs each script directly through EnergiBridge with no additional flags.
- **GPU version (GLG1 server)** - used specifically for G23 and G25 (15 codes run), which required execution on the secondary, GPU-equipped server. This version adds the `--gpu` flag to EnergiBridge to capture GPU energy metrics, and pipes the script's output through `head` to limit console clutter from GPU-related logging.

## Usage
IMPORTANT: We copy pasted the contents of these files into the server's terminal directly; they can also be moved to the server, executed correctly and ran directly on the remote environment.
To run a different benchmark or guideline, edit the following at the top of the script:

```bash
N_VALUE=25000

scripts=(
    "bs_g8.py"
    #"scimark_g27.py"
)
```

- `N_VALUE` - the input parameter passed to the benchmark script.
- `scripts` - the list of benchmark/guideline script(s) to run. Uncomment or add entries to include more versions in the same batch.
- The results folder name (e.g., `results-bubble-sort`, `glg1-mnd`) should also be updated at the top of the script to match the benchmark being tested.
- Comment/uncomment `N_VALUE` depending on the benchmark's needs.
- Make sure to change these values everywhere they appear in the script!

Each script produces one subfolder per entry in `scripts`, containing 30 `run_N.csv` files with the raw EnergiBridge output for that version.
