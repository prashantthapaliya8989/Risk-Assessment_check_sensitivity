#function to calculate rank
def array_rank_transform(arr):       
    sorted_list = sorted(arr)
    rank = 1
    # seed initial rank as 1 because that's first item in input list
    sorted_rank_list = [1]
    for i in range(1, len(sorted_list)):
        if sorted_list[i] != sorted_list[i-1]:
            rank += 1
        sorted_rank_list.append(rank)
    rank_list = []
    for item in arr:
        for index, element in enumerate(sorted_list):
            if element == item:
                rank_list.append(sorted_rank_list[index])
                # we want to break out of inner for loop
                break
    return rank_list