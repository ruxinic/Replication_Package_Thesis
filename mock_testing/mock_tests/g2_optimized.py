def process_data_optimized(data_list):
    # G2: Check if already sorted to avoid redundant operations
    # all() with a generator is an early-termination check
    if all(data_list[i] <= data_list[i+1] for i in range(len(data_list)-1)):
        return data_list
    
    data_list.sort()
    return data_list

my_data = [1, 2, 3, 4, 5] # Already sorted
result = process_data_optimized(my_data) # Skips the sort entirely