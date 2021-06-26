def get_min_max(value_list):    
    min_max = []
    
    for i in range(len(value_list)):
        empty = []
        minimum = round(min(value_list[i]),3) 
        maximum = round(max(value_list[i]),3)
        empty.append(minimum)
        empty.append(maximum)
        min_max.append(empty) 
    return (min_max)