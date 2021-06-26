def get_column_value(df):
    no_of_param = int(input("Enter number of useful column: "))

    filter_index_list = []
    select_index = int(input("Enter the index of subbasin: "))
    filter_index_list.append(select_index)
    for i in range(1,no_of_param):

        select_index = int(input("Enter the {} index: ".format(i)))
        filter_index_list.append(select_index)

    value_list = []

    # filter_index_list = [6,7,8,9,10]

    for i in range(no_of_param):
    # for i in range(5):

        empty = []
        for index, row in df.iterrows():
            # value = row[filter_index_list[i]]
            value = row[filter_index_list[i]]
            empty.append(value)
        value_list.append(empty)
    return (value_list)