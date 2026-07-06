import random

def selection_sort_g2(lst):
    for i, e in enumerate(lst):
        mn = min(range(i, len(lst)), key=lst.__getitem__)
        # G2: conditional guard avoids memory write 
        # operations if the element is already perfectly positioned
        if mn != i:
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

PARAM_SIZE = 30000
PARAM_DATA_TYPE = 'semi-sorted'

# Generate parameterized collection
my_list = generate_test_data(PARAM_SIZE, PARAM_DATA_TYPE)

# Execute sorting routine
sorted_result = selection_sort_g2(my_list)
