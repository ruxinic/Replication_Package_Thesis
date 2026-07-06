def expensive_check(data):
    return sum(i**2 for i in data) > 1000

def process_g4_optimized(my_list):
    # G4: Short-circuit logic. expensive_check ONLY runs if len > 0
    if len(my_list) > 0 and expensive_check(my_list):
        return True
    return False

data = list(range(100))
process_g4_optimized(data)