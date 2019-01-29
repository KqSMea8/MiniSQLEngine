import sys

# find index of a column in actual table
def find_index_column(col,table_cols):
    return_index = -1
    index = 0

    for col_n in table_cols:
        if col_n.endswith("."+col) or col_n.lower() == col.lower():
            return_index = index
            break
        index=index+1

    return return_index


# take column list as argument and return list index corresponds to column
def get_index_of_column(column,table_cols,join_table):

    if len(table_cols) == 0:
        return []

    column_index = []
    if ''.join(column) == '*':
        column = table_cols
    # print column
    for col in column:
        try:
            column_index.append(table_cols.index(col))
        except ValueError:
            common_column = 0
            search = ""
            for cl in table_cols:
                if cl.endswith("."+col):
                    common_column = common_column + 1
                    search = cl

            if(common_column == 1):
            	if search == "":
            		print "Wrong column name"
            		sys.exit()
                index = table_cols.index(search)
                column_index.append(index)
            else:
                return []

    if(len(join_table)>0):
        for i in range(len(join_table)):
            if join_table[i][0] in column_index and join_table[i][1] in column_index:
                i1 = column_index.index(join_table[i][0])
                i2 = column_index.index(join_table[i][1])
                if i1>i2:
                    del column_index[i1]
                else:
                    del column_index[i2]

    if(len(column_index) == 0):
        print "Error in columns syntax"
        sys.exit()

    return column_index