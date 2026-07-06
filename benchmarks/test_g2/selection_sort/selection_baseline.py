import random
def selection_sort(lst):
    for i, e in enumerate(lst):
        mn = min(range(i,len(lst)), key=lst.__getitem__)
        lst[i], lst[mn] = lst[mn], e
    return lst

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


# change these parameters:
PARAM_SIZE = 30000
PARAM_DATA_TYPE = 'semi-sorted'

# Generate parameterized collection
my_list = generate_test_data(PARAM_SIZE, PARAM_DATA_TYPE)

# Execute sorting routine
sorted_result = selection_sort(my_list)