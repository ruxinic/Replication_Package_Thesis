rm -rf glg1-mnd
mkdir -p glg1-mnd

N_VALUE=6000

scripts=(
    "mnd_ros_baseline.py"
)

#temporary task list for 30 repetitions of each file
task_list="all_tasks.txt"
> "$task_list"

for script in "${scripts[@]}"; do
    #check the file exists before adding it to the list
    if [ -f "$script" ]; then
        folder_name=$(echo "$script" | cut -d'.' -f1)
        mkdir -p "glg1-mnd/$folder_name"
        for i in {1..30}; do
            echo "$script $folder_name $i" >> "$task_list"
        done
    else
        echo "Warning: $script not found in current directory. Skipmndng."
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
    
    energibridge --gpu --output "glg1-mnd/$folder/run_$iteration.csv" python3 "$script" "$N_VALUE" 2>&1 | head
    if [ "$current_run" -lt "$total_runs" ]; then
        echo "Cooling down for 30 seconds..."
        sleep 30
    fi
    
    ((current_run++))
done < "$task_list"
rm "$task_list"
echo "All experiments completed successfully!"