from utils.get_normalized_value import get_normalized_value
from utils.get_column_value import get_column_value
from utils.get_column_name import get_column_name
from utils.get_min_max import get_min_max
from utils.array_rank_transform import array_rank_transform
from utils.get_sd_and_compute import get_sd_and_compute
from utils.get_sd_and_compute_geogenic import get_sd_and_compute_geogenic
from utils.get_rank_class import get_rank_class

import geopandas, statistics, random, copy
import pandas as pd
from statistics import mean

############    Climate    ############
############    Climate    ############
############    Climate    ############
print ("\n \n")
print ("Climate")
print ()

climate = 'D:/ICIMOD/Additional Data/others/2021/VARA/Shortcut/shp/kailash_sb_climate.shp'

file = open(climate)
df = geopandas.read_file(climate)

column = get_column_name(climate)
column_value = get_column_value(df)
min_max = get_min_max(column_value)
norm = get_normalized_value(column_value,min_max)

#average of inter and intra, precipitation and temperature + their combined
def cal_mean(a,b): #a function that calculates mean
    d = (a,b)
    return mean(d)

climate_avg = []
climate_avg.append(column_value[0])
for i in range(2):
    empty = []
    for index in range(len(norm[0])):
        avg = round( (cal_mean(norm[i+1][index],norm[i+3][index])), 3 )
        empty.append(avg)
#         print (norm[i+4][index])
    climate_avg.append(empty)

empty1 = []
for index in range(len(norm[0])):
    avg1 = round( (cal_mean(climate_avg[1][index],climate_avg[2][index])), 3 )
    empty1.append(avg1)
climate_avg.append(empty1)
# print (climate_avg)     #[subbasin, avgP, avgT, avgC]

min_max1 = get_min_max(climate_avg)
norm1 = get_normalized_value(climate_avg,min_max1)
c_norm11 = []                              #[[subbasin], [cli_norm]] 
c_norm11.append(column_value[0])
c_norm11.append(norm1[3])


#########    Geogenic      ##########
#########    Geogenic      ##########
#########    Geogenic      ##########

print ("\n \n")
print("Geogenic")
print ()

geogenic = 'D:/ICIMOD/Additional Data/others/2021/VARA/Shortcut/shp/kailash_sb_geogenic.shp'

g_file = open(geogenic)
g_df = geopandas.read_file(geogenic)

g_column = get_column_name(geogenic)
g_column_value = get_column_value(g_df)
g_min_max = get_min_max(g_column_value)
g_norm = get_normalized_value(g_column_value,g_min_max)

#generating the average of all geogenic hazards
geogenic_avg = []

geogenic_avg.append(g_norm[0])
empty1 = []
for i in range(len(g_norm[0])):
    empty = []
    for index in range(len(g_norm)-1):
        value = g_norm[index+1][i]
        empty.append(value)
    t_empty = tuple(empty)
    m = round(mean(t_empty),3)
    empty1.append(m)
geogenic_avg.append(empty1)

g_min_max1 = get_min_max(geogenic_avg)
g_norm1 = get_normalized_value(geogenic_avg,g_min_max1)
# print (len(g_norm1))       #2
g_norm11 = []                        #[[subbasin], [geo_norm]]
g_norm11.append(g_column_value[0])
g_norm11.append(g_norm1[1])



#########    Adaptive Capacity      ##########
#########    Adaptive Capacity      ##########
#########    Adaptive Capacity      ##########

print ("\n \n")
print("Adaptive Capacity")
print ()

ac = 'D:/ICIMOD/Additional Data/others/2021/VARA/Shortcut/shp/kailash_sb_AC.shp'

ac_file = open(ac)
ac_df = geopandas.read_file(ac)

ac_column = get_column_name(ac)
ac_column_val = get_column_value(ac_df)     
ac_column_value = []
ac_column_value.append(ac_column_val[0])
empty = []
for i in range(len(ac_column_val[1])):
    value = 5 - ac_column_val[1][i]
    empty.append(value)
ac_column_value.append(empty)           #[[subbasin],[AC_norm]]

#########    Exposure      ##########
#########    Exposure      ##########
#########    Exposure      ##########

print ("\n \n")
print("Exposure")
print ()

exp = 'D:/ICIMOD/Additional Data/others/2021/VARA/Shortcut/shp/kailash_sb_exposure.shp'

exp_file = open(exp)
exp_df = geopandas.read_file(exp)

exp_column = get_column_name(exp)
exp_column_value = get_column_value(exp_df)     #[[subbasin],[exp]]


#########    Sensitivity      ##########
#########    Sensitivity      ##########
#########    Sensitivity      ##########

print ("\n \n")
print("Sensitivity")
print ()

sen = 'D:/ICIMOD/Additional Data/others/2021/VARA/Shortcut/shp/kailash_sb_sensitivity.shp'

sen_file = open(sen)
sen_df = geopandas.read_file(sen)

sen_column = get_column_name(sen)
sen_column_value = get_column_value(sen_df)     #[[subbasin],[exp]]

##Calculation of rank of the original value
final_score = []
final_score.append(sen_column_value[0])
empty = []
for i in range(len(sen_column_value[0])):
    avg = round((c_norm11[1][i] + g_norm11[1][i]) / 2 ,3)
    product = round( avg * ac_column_value[1][i] * exp_column_value[1][i] * sen_column_value[1][i], 3)
    empty.append(product)
final_score.append(empty)

final_min_max = get_min_max(final_score)
final_norm = get_normalized_value(final_score, final_min_max)
final_norm.append(array_rank_transform(final_norm[1]))

final_norm_filter = []   #filter by removing the zero term
for i in range(len(final_norm)):
    empty = []
    for index in range(len(final_norm[0])):
        if (final_norm[1][index] != 0):
            empty.append(final_norm[i][index])
    final_norm_filter.append(empty)

rank = []
rank.append(final_norm_filter[0])
rank.append(array_rank_transform(final_norm_filter[1]))

r = array_rank_transform(final_norm_filter[1])

# # dict = {'sub': final_norm[0], 'climate': c_norm11[1], 'geo': g_norm11[1],
# #             'ac': ac_column_value[1], 'exp': exp_column_value[1], 'sen': sen_column_value[1],
# #             'fin_scr': final_score[1],'norm': final_norm[1], 'rank': rank[1]}
# # pd.DataFrame(data=dict).to_csv('D:/ICIMOD/Additional Data/others/2021/VARA/Shortcut/new/try_final.csv', index=False)

########## Computing each original value of climate and geogenic ############
########## by 1 SD 
print("\n \n \n")
num = int(input("Enter the number of check:"))
print("\n \n")

#initialize class variable
# cls = [20,40,60,80]
cls_input = int(input("{Example: for 4 input value, there will be 5 classses\n"
                        "[20,30,40,50] = <20, 20-30, 30-40, 40-50, >50}\n\n"
                        "Enter the number of classses: "))
cls = []
for i in range(cls_input):
    val = int(input("Enter the {} class: ".format(i+1)))
    cls.append(val)
cls.append(99999)
# print(cls)
cls_val = []
empty = []
for index in range(len(rank[0])):
    empty.append(0)
    
for i in range(len(cls)):
    em = copy.deepcopy(empty)
    cls_val.append(em) 
# print (cls_val)    
#[[0, 0, 0, 0, ....], [0, 0, 0, 0, ...], [0, 0, 0, 0, ...], [0, 0, 0, 0, ...], [0, 0, 0, 0, ...]]

for i in range(num):
    ####### Climate #############

    compute_sd = get_sd_and_compute(column_value)
    min_max = get_min_max(compute_sd)
    norm = get_normalized_value(compute_sd,min_max)

    #average of inter and intra, precipitation and temperature + their combined
    def cal_mean(a,b): #a function that calculates mean
        d = (a,b)
        return mean(d)

    climate_avg = []
    climate_avg.append(column_value[0])
    for i in range(2):
        empty = []
        for index in range(len(norm[0])):
            avg = round( (cal_mean(norm[i+1][index],norm[i+3][index])), 3 )
            empty.append(avg)
    #         print (norm[i+4][index])
        climate_avg.append(empty)

    empty1 = []
    for index in range(len(norm[0])):
        avg1 = round( (cal_mean(climate_avg[1][index],climate_avg[2][index])), 3 )
        empty1.append(avg1)
    climate_avg.append(empty1)
    # print (climate_avg)     #[subbasin, avgP, avgT, avgC]

    min_max1 = get_min_max(climate_avg)
    norm1 = get_normalized_value(climate_avg,min_max1)
    c_norm11 = []                              #[[subbasin], [cli_norm]] 
    c_norm11.append(column_value[0])
    c_norm11.append(norm1[3])


    ####### Geogenic #############
    g_compute_sd = get_sd_and_compute_geogenic(g_column_value)
    g_min_max = get_min_max(g_compute_sd)
    g_norm = get_normalized_value(g_compute_sd,g_min_max)


    #generating the average of all geogenic hazards
    geogenic_avg = []

    geogenic_avg.append(g_norm[0])
    empty1 = []
    for i in range(len(g_norm[0])):
        empty = []
        for index in range(len(g_norm)-1):
            value = g_norm[index+1][i]
            empty.append(value)
        t_empty = tuple(empty)
        m = round(mean(t_empty),3)
        empty1.append(m)
    geogenic_avg.append(empty1)

    g_min_max1 = get_min_max(geogenic_avg)
    g_norm1 = get_normalized_value(geogenic_avg,g_min_max1)
    # print (len(g_norm1))       #2
    g_norm11 = []                        #[[subbasin], [geo_norm]]
    g_norm11.append(g_column_value[0])
    g_norm11.append(g_norm1[1])

    ##Calculation of rank of the original value
    final_score = []
    final_score.append(sen_column_value[0])
    empty = []
    for i in range(len(sen_column_value[0])):
        avg = round((c_norm11[1][i] + g_norm11[1][i]) / 2 ,3)
        product = round( avg * ac_column_value[1][i] * exp_column_value[1][i] * sen_column_value[1][i], 3)
        empty.append(product)
    final_score.append(empty)

    final_min_max = get_min_max(final_score)
    final_norm = get_normalized_value(final_score, final_min_max)
    final_norm.append(array_rank_transform(final_norm[1]))

    final_norm_filter = []   #filter by removing the zero term
    for i in range(len(final_norm)):
        empty = []
        for index in range(len(final_norm[0])):
            if (final_norm[1][index] != 0):
                empty.append(final_norm[i][index])
        final_norm_filter.append(empty)
    
    new_rank = array_rank_transform(final_norm_filter[1])
    # print(new_rank)
    rank.append(array_rank_transform(final_norm_filter[1]))
    diff = []
    # print (len(final_norm_filter[1]))
    # print ("new_rank", new_rank[1], len(new_rank))
    # print ("r", r , len(r))
    for i in range(len(final_norm_filter[1])):
        value = abs(r[i] - new_rank[i])
        diff.append(value)
    rank.append(diff)
    # print  (len(diff), diff)

    for i in range(len(diff)):
        a = get_rank_class(diff[i],cls)
        
        cls_val[a][i] = cls_val[a][i]+1
        # print (diff[i], a)
# print ("cls_val", cls_val)

#Store the classes in a dictionary
dict = {}
dict["Subbasin"] = rank[0]
for i in range(len(cls_val)):
    if (i == 0):
        dict["<{}".format(cls[i])] = cls_val[i]
    elif (i == len(cls_val)-1):
        dict[">{}".format(cls[i-1])] = cls_val[i]
    else:
        dict["{}-{}".format(cls[i-1], cls[i])] = cls_val[i]
# print (dict)

pd.DataFrame(data=dict).to_csv('D:/ICIMOD/Additional Data/others/2021/VARA/Shortcut/new/climate_class.csv', index=False)



# print (rank)
# Store the  values of rank and their difference in a dictionary
dict = {}
for i in range(len(rank)):
    if (i==0):
        dict["Subbasin"] = rank[i]
    elif (i==1):
        dict["Original rank"] = rank[i]
    elif (i%2==0):
        dict["rank{}".format(int(i/2))] = rank[i]
    else:
        dict["diff{}".format(int((i-1)/2))] = rank[i]
        

# print (dict)

pd.DataFrame(data=dict).to_csv('D:/ICIMOD/Additional Data/others/2021/VARA/Shortcut/new/try_final.csv', index=False)
