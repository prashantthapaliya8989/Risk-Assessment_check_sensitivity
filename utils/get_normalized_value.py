def get_normalized_value(value_list, min_max):    
    norm = []
    norm.append(value_list[0])
    for i in range(len(value_list)-1):
        empty = []
        for index in range(len(value_list[0])):
            diff = round (min_max[i+1][1] - min_max[i+1][0], 3)
            value = round( ((value_list[i+1][index]-min_max[i+1][0])/diff) , 3)
            empty.append(value)
        
        norm.append(empty)
    # for i in range(len(norm[0])):
    #     print (norm[0][i], norm[1][i], norm[2][i], norm[3][i], norm[4][i])
    return (norm)