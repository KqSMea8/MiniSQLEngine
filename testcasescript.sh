# python2 run.py "$1"
python2 run.py "select max(A) from table1;" >> q1.txt
python2 run.py "select min(B) from table2;" >> q2.txt
python2 run.py "select avg(C) from table1;" >> q3.txt
python2 run.py "select sum(D) from table2;" >> q4.txt
python2 run.py "select A,D from table1,table2;" >> q5.txt
python2 run.py "select distinct(C) from table1;" >> q6.txt
python2 run.py "select B,C from table1 where A=-900;" >> q7.txt
python2 run.py "select A,B from table1 where A=775 OR B=803;" >> q8.txt
python2 run.py "select * from table1,table2;" >> q9.txt
python2 run.py "select * from table1,table2 where table1.B=table2.B;" >> q10.txt
python2 run.py "select A,D from table1,table2 where table1.B=table2.B;" >> q11.txt
python2 run.py "select table1.C from table1,table2 where table1.A<table2.B;" >> q12.txt
python2 run.py "select A from table4;" >> q13.txt
python2 run.py "select Z from table1;" >> q14.txt
python2 run.py "select B from table1,table2;" >> q15.txt
python2 run.py "select distinct A,B from table1;" >> q16.txt
python2 run.py "select table1.C from table1,table2 where table1.A<table2.D OR table1.A>table2.B;" >> q17.txt
python2 run.py "select table1.C from table1,table2 where table1.A=table2.D;" >> q18.txt
python2 run.py "select table1.A from table1,table2 where table1.A<table2.B AND table1.A>table2.D;" >> q19.txt
python2 run.py "select sum(table1.A) from table1,table2;" >> q20.txt
