def expensive_check(data):
    # Simulate a heavy computation
    return sum(i**2 for i in data) > 1000

def process_g4_baseline(my_list):
    # BOTH conditions are evaluated or the expensive one is checked unnecessarily
    # Here, we might accidentally use a method that doesn't short-circuit efficiently
    check_1 = len(my_list) > 0
    check_2 = expensive_check(my_list) #here its computed anyways
    
    if check_1 and check_2:
        return True
    return False

data = list(range(100))
process_g4_baseline(data)