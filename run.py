import sys

import validate_query as vq
import read_data as rd

table_schema={}
sql_query = sys.argv[1]
sql_query = sql_query.split(";")[0]
sql_query.strip()
table_schema=rd.read_meta_data(table_schema)
vq.validate_query(sql_query,table_schema)