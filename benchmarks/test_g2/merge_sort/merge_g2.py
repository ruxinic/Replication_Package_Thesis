import random

def merge_sort(m):
    if len(m) <= 1:
        return m

    middle = len(m) // 2
    left = m[:middle]
    right = m[middle:]

    left = merge_sort(left)
    right = merge_sort(right)
    
    #G2: if left's highest value <= right's lowest value, skipping merge is safe
    if left[-1] <= right[0]:
        return left + right  # bypass the entire expensive while loop below

    return merge(left, right)

def merge(left, right):
    # G2: if the largest item in 'left' is smaller than or equal to the smallest 
    # item in 'right', the combined collection is already perfectly sorted
    if left[-1] <= right[0]:
        return left + right  
    result = []
    left_idx, right_idx = 0, 0
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] <= right[right_idx]:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1

    if left_idx < len(left):
        result.extend(left[left_idx:])
    if right_idx < len(right):
        result.extend(right[right_idx:])
    return result

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

PARAM_SIZE = 9000000
PARAM_DATA_TYPE = 'semi-sorted' 

if __name__ == "__main__":
    # Generate the dataset
    my_list = generate_test_data(PARAM_SIZE, PARAM_DATA_TYPE)

    sorted_result = merge_sort(my_list)
    print(sorted_result)

