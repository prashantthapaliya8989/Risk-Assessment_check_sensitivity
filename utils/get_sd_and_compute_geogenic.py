import statistics, random


def get_sd_and_compute_geogenic(value_list):
    sd_list = []
    for i in range(len(value_list)-1):
        value = round(statistics.stdev(value_list[i+1]),3)
        sd_list.append(value)
    # print (sd_list)

    compute_list = []
    for i in range(1):
        empty = value_list[i]
        compute_list.append(empty)
    for i in range(len(value_list)-1):
        empty = []
        for index in range(len(value_list[0])):
            if (value_list[i+1][index] > 0.02):
                random_num =  0.5 #random.randrange(-1000, 1000, 4)/1000
                value = round((value_list[i+1][index] + random_num * sd_list[i]), 3)
                empty.append(value)
            else:
                value = 0
                empty.append(value)
        compute_list.append(empty)
    return (compute_list)
