import geopandas

def get_column_name(shp):
    file = open(shp)
    df = geopandas.read_file(shp)

    print ("The columns of the table are: ")
    count = 0
    column_List = []
    for i in range(len(df.columns)):
        print (str(count) + '    ' + df.columns[i])
        count += 1
        column_List.append(df.columns[i])
    return (column_List)