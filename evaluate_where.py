import sys,re
import find_index as fi

# evaluate where condition
def where_check(condition,table_cols,final_result):

    try:
	    arr = condition.split(" ")
	    arr = map(str.strip,arr)
	    connector = []
	    for ar in arr:
	        if ar.lower().strip() == "and" or ar.lower().strip() == "or":
	            connector.append(ar.lower().strip())

	    delimiters="or","and"
	    regexPattern = '|'.join(map(re.escape, delimiters))+"(?i)"
	    con = re.split(regexPattern, condition)
	    con = map(str.strip,con)

	    for i in range(len(con)) :

	        operandslist = get_operands(con[i])
	        operandslist = map(str.strip,operandslist)
	        # print operandslist[0],operandslist[1]
	        # print table_cols
	        lhs = fi.find_index_column(operandslist[0].strip(),table_cols)
	        rhs = fi.find_index_column(operandslist[1].strip(),table_cols)
	        # print lhs,rhs
	        if lhs >-1 and rhs >-1:
	            operandslist[0] = operandslist[0].replace(operandslist[0],"final_result[i]["+str(lhs)+"]")
	            operandslist[1] = operandslist[1].replace(operandslist[1],"final_result[i]["+str(rhs)+"]")

	        elif lhs>-1:
	            operandslist[0] = operandslist[0].replace(operandslist[0],"final_result[i]["+str(lhs)+"]")

	        else:
	        	# print "EW"
	        	print "Error in syntax"
	        	sys.exit()

	        t = operandslist[0],operandslist[1]
	        con[i] = operandslist[2].join(t)

	    new_con = con[0]+" "

	    andor = 0
	    for j in range(1,len(con)):
	        new_con+= connector[andor].lower()+" "
	        new_con+=con[j]+" "
	        andor = andor + 1

	    res = []

	    for i in range(len(final_result)):
	        if eval(new_con):
	            res.append(final_result[i])

    except Exception as e:
    	# print "EW"
        print "Error in syntax"
        sys.exit()

    return res

# get operator
def get_operator(con):

    relational_operator = ""
    i=0

    while i< len(con):

    	if con[i] == "=" and (con[i+1] != "=" or con[i+1] != "<" or con[i+1] != ">" or con[i+1] != "!"):
            relational_operator = "="
            i+=1
        elif con[i] == "<" and con[i+1] == "=":
            relational_operator = "<="
            i+=1
        elif con[i] == "<" and con[i+1] != "=":
            relational_operator = "<"
            i+=1
        elif con[i] == "!" and con[i+1] == "=":
            relational_operator = "!="
            i+=1
        elif con[i] == ">" and con[i+1] == "=":
            relational_operator = ">="
            i+=1
        elif con[i] == ">" and con[i+1] != "=":
            relational_operator = ">"
            i+=1
        i+=1
    return relational_operator


# get operands
def get_operands(con):
    operands_list = []
    try:
        relational_operator = get_operator(con)
        if relational_operator == "":
        	print "Unknown operator"
        	sys.exit()

        operands_list = con.split(relational_operator)
        operands_list = map(str.strip,operands_list)
        if relational_operator != "=":
            operands_list.append(relational_operator)
        else:
            operands_list.append("==")

    except:
        print "Syntax Error in where condition"
        sys.exit()

    return operands_list