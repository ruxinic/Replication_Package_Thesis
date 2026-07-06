rm -rf results-bubble-sort
mkdir -p results-bubble-sort

N_VALUE=25000  

scripts=(
    "bs_g8.py"
    #"scimark_g27.py"
)

#temporary task list for 30 repetitions of each file
task_list="all_tasks.txt"
> "$task_list"

for script in "${scripts[@]}"; do
    #check the file exists before adding it to the list
    if [ -f "$script" ]; then
        folder_name=$(echo "$script" | cut -d'.' -f1)
        mkdir -p "results-bubble-sort/$folder_name"
        for i in {1..30}; do
            echo "$script $folder_name $i" >> "$task_list"
        done
    else
        echo "Warning: $script not found in current directory."
    fi
done

shuf "$task_list" -o "$task_list"

total_runs=$(wc -l < "$task_list")
current_run=1

echo "Starting $total_runs randomized runs with 30s cool-down..."

while read -r script folder iteration; do
    echo "------------------------------------------------"
    echo "Progress: $current_run / $total_runs"
    echo "Running: $script (Iteration $iteration)"
    
    energibridge --output "results-bubble-sort/$folder/run_$iteration.csv" python3 "$script" "$N_VALUE"
    if [ "$current_run" -lt "$total_runs" ]; then
        echo "Cooling down for 30 seconds..."
        sleep 30
    fi
    
    ((current_run++))
done < "$task_list"
rm "$task_list"
echo "All experiments completed successfully!"