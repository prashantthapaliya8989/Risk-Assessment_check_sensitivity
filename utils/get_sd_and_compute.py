import statistics, random

def get_sd_and_compute(value_list):
    #Compute SD
    sd_list = []
    for i in range(len(value_list)-1):
        value = round(statistics.stdev(value_list[i+1]),3)
        sd_list.append(value)
    # print (sd_list)

    #Compute with 1 SD
    compute_list = []
    compute_list.append(value_list[0])
    for i in range(len(value_list)-1):
        empty = []
        for index in range(len(value_list[0])):
            random_num =  0.5 #random.randrange(-1000, 1000, 4)/1000
            value = round((value_list[i+1][index] + random_num * sd_list[i]), 3)
            empty.append(value)
        compute_list.append(empty)
    return (compute_list)
    # print (compute_list)