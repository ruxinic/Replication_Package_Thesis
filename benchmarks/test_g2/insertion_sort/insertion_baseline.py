import random
def insertion_sort(L):
    for i, value in enumerate(L):
        for j in range(i - 1, -1, -1):
            if L[j] > value:
                L[j + 1] = L[j]
                L[j] = value
    return L

def generate_test_data(size, data_type='random'):
    """
    Generates distinct list variations based on parameter.
    Available options for data_type: 'sorted', 'semi-sorted', 'reversed', 'random'
    """
    if data_type == 'sorted':
        return list(range(size))
        
    elif data_type == 'reversed':
        return list(range(size, 0, -1))
        
    elif data_type == 'semi-sorted':
        lst = list(range(size))
        break_point = int(size * 0.9)
        shuffled_part = lst[break_point:]
        random.shuffle(shuffled_part)
        lst[break_point:] = shuffled_part
        return lst
        
    else:  # 'random'
        lst = list(range(size))
        random.shuffle(lst)
        return lst

# Change these values to test different scenarios
PARAM_SIZE = 10000
PARAM_DATA_TYPE = 'semi-sorted'  # Try: 'sorted', 'semi-sorted', 'random', 'reversed'

if __name__ == "__main__":
    my_list = generate_test_data(PARAM_SIZE, PARAM_DATA_TYPE)

    sorted_result = insertion_sort(my_list)

    print("Sorted result:")
    print(sorted_result)