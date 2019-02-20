import sys,os,re,sqlparse,csv

import find_index as fi
import seperate_column as sc
import evaluate_where as ew
import read_data as rd
from read_data import *

# if sqlparser not there in os then it will automatically locate
sys.path.insert(0,os.getcwd() + "/sqlparse")
final_result = []
table_cols = []
join_table = []

# validate query function
def validate_query(query,table_schema):

    global table_cols,final_result
    parsed_query = sqlparse.parse(query)[0].tokens
    command = sqlparse.sql.Statement(parsed_query).get_type()

    # if not select command
    if command.lower() != 'select':
        print "Query is not valid"
        sys.exit()

    # divide query in component
    # 1 command (select)
    # 2 distinct if present
    # 3 column list
    # 4 from
    # 5 table name
    # 6 where condition
    components = []
    c = sqlparse.sql.IdentifierList(parsed_query).get_identifiers()
    for i in c:
        components.append(str(i))

    dist = 0			# distinct flag
    where = 0			# where flag
    table_names = ""	# store table list comma seperated(present in query)
    condition = ""		# store string after where 
    cols = ""			# store column list comma seperated(present in query)

    if len(components) < 4:
        # print "VQ-1"
    	print "Error in syntax"
    	sys.exit()

    for i in range(len(components)):
        if components[i].lower() == "distinct":
            dist=dist+1
        elif components[i].lower() == "from":
            table_names = components[i+1]
        elif components[i].lower().startswith("where"):
            where=1
            condition = components[i][6:].strip()

    # distict clause should not present more than one time
    if(dist>1):
        print "Error in distinct syntax"
        sys.exit()

    # if condition not present but where clause present
    if where == 1 and len(condition.strip())==0:
        print "Error in where clause"
        sys.exit()

    # if where clause not present and still query can be divided into more than 5 comp. then something
    # must be missing
    if len(components)> 5 and where ==0 :
        # print "VQ-2"
        print "Error in syntax"
        sys.exit()

    # if 5 components but no where and no distinct clause then something missing or something extra
    # present in query.
    if len(components)== 5 and where ==0 and dist==0:
        # print "VQ-3"
        print "Error in syntax"
        sys.exit()

    # if distinct clause present then column list become 3rd component of the query
    # else second component of the query
    if dist == 1:
        cols_with_aggr = components[2]
    else:
        cols_with_aggr = components[1]

    column = []
    aggr = []

    # seperate column name in aggregate function list and column list
    sc.get_aggregate_column_list(cols_with_aggr,column,aggr)

    table_names = table_names.split(",")
    table_names = map(str.strip,table_names)

    # get column list from table list
    table_cols=[]
    table_cols=sc.query_table_cols(table_names,table_cols,table_schema)

    final_result = []
    table_dot_column_list_print = ""

    final_result = join(table_names,dist)

    # Where condition presents
    if condition != "":
        final_result = ew.where_check(condition,table_cols,final_result)

        # If there are aggregate functions with where condition
        if len(aggr)>0:
            col_index_list = fi.get_index_of_column(column,table_cols,join_table)
            for i in range(len(col_index_list)):
                table_dot_column_list_print+=aggr[i]+"("+table_cols[col_index_list[i]]+")," # heading contains list of columns in the
                																# form of table name.column name
            table_dot_column_list_print = table_dot_column_list_print[:-1]
            table_dot_column_list_print = table_dot_column_list_print+"\n"
        natural_join(condition,join_table,table_cols)
    ans = ""

    # if aggregate function not present in the query
    if len(aggr) == 0:
        resultant_col = fi.get_index_of_column(column,table_cols,join_table)
        if len(resultant_col) == 0:
            # print "VQ-4"
            print "Error in syntax"
            sys.exit()
        table_dot_column_list_print = []
        for i in resultant_col:
            table_dot_column_list_print.append(table_cols[i])
        table_dot_column_list_print = ",".join(table_dot_column_list_print)
        table_dot_column_list_print += "\n"

        for i in range(len(final_result)):
            for j in range(len(resultant_col)):
                ans+=str(final_result[i][resultant_col[j]])+"\t"

            ans+="\n"

    # If aggregate function present
    else:
        try:
            table_dot_column_list_print = ""
            resultant_col = fi.get_index_of_column(column,table_cols,join_table)
            for i in range(len(resultant_col)):
                table_dot_column_list_print+=aggr[i]+"("+table_cols[resultant_col[i]]+"),"
            table_dot_column_list_print = table_dot_column_list_print[:-1]
            table_dot_column_list_print = table_dot_column_list_print+'\n'

            if len(table_dot_column_list_print)>0:
                ans+=aggregate_func(column,aggr)
            else:
                ans = "NULL"
        except IndexError as e:
            # print "VQ"
            print "Error in syntax"
            sys.exit()

    if dist == 1:
        ans = get_distinct_rows(ans)

    if ans == "":
        print "No data present"
    else:
        print table_dot_column_list_print+ans

# evaluate aggregate function for a given column and return answer of the agg. function
def aggregate_func(column,aggr):
    ans = ""
    for i in range(len(column)):
        if aggr[i].lower() == "max":
            indexlist = fi.get_index_of_column([column[i]],table_cols,join_table)
            index = indexlist[0]
            maxval= -9999999
            for i in range(len(final_result)):
                if maxval < final_result[i][index]:
                    maxval = final_result[i][index]

            ans+=str(maxval)+"\t"

        elif aggr[i].lower() == "min":
            indexlist = fi.get_index_of_column([column[i]],table_cols,join_table)
            index = indexlist[0]
            minval = 99999999
            for i in range(len(final_result)):
                if minval > final_result[i][index]:
                    minval = final_result[i][index]
                # temp.append()

            ans+=str(minval)+"\t"

        elif aggr[i].lower() == "sum":
            indexlist = fi.get_index_of_column([column[i]],table_cols,join_table)
            index = indexlist[0]
            totalsum = 0
            for i in range(len(final_result)):
                totalsum = totalsum + final_result[i][index]

            ans+=str(totalsum)+"\t"

        elif aggr[i].lower() == "avg":
            indexlist = fi.get_index_of_column([column[i]],table_cols,join_table)
            index = indexlist[0]
            avg = 0.0
            for i in range(len(final_result)):
                avg = avg + final_result[i][index]
            avg = avg/len(final_result)
            ans+=str(avg)+"\t"

    return ans


# this function returns distinct rows
def get_distinct_rows(ans):
    try:
        rows = ans.split("\n")
        distinct_row = []
        for singlerow in rows:
            if singlerow in distinct_row:
                continue
            distinct_row.append(singlerow)

        returnval = '\n'.join(distinct_row)

    except Exception:
        print "Error in syntax"
        sys.exit()

    return returnval

# function to join multiple tables
def join(table_names,distinct):
    if len(table_names) == 1:
        return rd.read_csv_form_table(table_names[0],distinct)
    else:
        table = rd.read_csv_form_table(table_names[0],distinct)
        for i in range(1,len(table_names)):
            t = rd.read_csv_form_table(table_names[i],distinct)
            temp_table = []
            for j in range(0,len(table)):
                for k in range(0,len(t)):
                    temp_table.append(table[j]+t[k])
            table = temp_table
    return table


# perform natural join operation
def natural_join(condition,join_table,table_cols):
    try:
        delimiters="or","and"
        regexPattern = '|'.join(map(re.escape, delimiters))+"(?i)"
        con = re.split(regexPattern, condition)
        con = map(str.strip,con)

        for i in range(len(con)):
            split = ew.get_operands(con[i])
            split = map(str.strip,split)

            if '.' in split[0] and '.' in split[1]:
                if split[2].strip() == "==":
                    same = fi.find_index_column(split[0].strip(),table_cols),fi.find_index_column(split[1].strip(),table_cols)
                    join_table.append(same)

    except Exception as e:
        # print "AAA"
        print "Error in syntax"
        sys.exit()
    return join_table