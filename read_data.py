import sys,csv

metafilename = "metadata.txt"

# Read meta data from metadata.txt
def read_meta_data(table_schema):		
    f = open(metafilename,"r")
    flag = None
    for line in f:
        if line.strip() == "<begin_table>":
            flag="get_table_name"
            columns = []
            continue
        if line.strip() == "<end_table>":
            table_schema[tablename] = columns
            columns = []
            continue
        if flag=="get_table_name":
            tablename=line.strip()
            flag="get_column_of_table"
            continue
        columns.append(line.strip())
    return table_schema

def read_csv_form_table(fname,distinct):
    fname = fname + ".csv"
    final_result = []
    # print fname
    try:
    	reader=csv.reader(open(fname),delimiter=',')
    except Exception, e:
    	# print "ABC"
        print "Query not formed properly"
        sys.exit()
    for row in reader:
        for i in range(len(row)):
            if row[i][0] == "\'" or row[i][0] == '\"':
                row[i] = row[i][1:-1]
                # print row[i]
        row = map(str.strip,row)
        row = map(int,row)


        if distinct == 1:
            if row not in final_result:
                final_result.append(row)
        else:
            final_result.append(row)

    return final_result