from read_data import *
import sys

# seperate aggregate function from column name and create new column list and aggregate function list
def get_aggregate_column_list(cols,column,aggr):

    cols = cols.split(",")
    cols = map(str.strip,cols)
    flag = None
    for i in range(len(cols)):
        if cols[i].lower().startswith("min") or cols[i].lower().startswith("max") or cols[i].lower().startswith("avg") or cols[i].lower().startswith("sum"):
            aggr.append(cols[i].split("(")[0])
            column.append(cols[i][4:len(cols[i])-1])
            flag = "Aggr_present"
        else:
            if flag == None:
            	column.append(cols[i])
            else:
            	print "Some column has aggregate function some column does not have... Error!!!"
            	sys.exit()

# it returns the list of columns of a given table list
# return table_name.column_name
def query_table_cols(table_names,table_cols,table_schema):

    for i in range(len(table_names)):
        if table_names[i] in table_schema:
            schema = table_schema[table_names[i]]
            for j in range(len(schema)):
                table_cols.append(table_names[i]+"."+schema[j])

        else:   # if table does not exist then error in query hence return none list
            print "Table does not exist in schema"
            sys.exit()

    return table_cols