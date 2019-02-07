from subprocess import Popen, PIPE
import re
import os
#creating dictionary for the variables
a={}
counter =1
for i in range(1,10):
    for j in range(1,10):
        for k in range(1,10):
            index_string = str(i)+str(j)+str(k)
            index_int = int(index_string)
            a[index_int]=counter
            counter = counter +1
#Encoding
dimacsFile = os.path.abspath(os.path.join(os.getcwd(),'sudoku_dimacs.cnf'))
f = open(dimacsFile,"w")
f.write("c Sudoku SAT Encodings for 9x9 grid\n")
f.write("p CNF 729 \n")
#There is atleast one number in each entry
for i in range(1,10):
    for j in range(1,10):
        line = ""
        for k in range(1,10):
            index_string=str(i)+str(j)+str(k)
            index_int =int(index_string)
            line=line+str(a[index_int])+" "
        line = line+ str(0)
        f.write(line+"\n")
#There is atmost one number in each entry
for i in range(1,10):
    for j in range(1,10):
        for k in range(1,9):
            for l in range(k+1,10):
                index_string_1 = str(i)+str(j)+str(k)
                index_int_1 =int(index_string_1)
                index_string_2 = str(i)+str(j)+str(l)
                index_int_2 = int(index_string_2)
                line = "-"+str(a[index_int_1])+" "+"-"+str(a[index_int_2])+" 0"
                f.write(line+"\n")
#Each number appears atmost once in each row
for x in range(1,10):
    for z in range(1,10):
        for y in range(1,9):
            for i in range(y+1,10):
                index_string_1 = str(x)+str(y)+str(z)
                index_string_2 = str(x)+str(i)+str(z)
                index_int_1=int(index_string_1)
                index_int_2=int(index_string_2)
                line="-"+str(a[index_int_1])+" -"+str(a[index_int_2])+" 0"
                f.write(line+"\n")
#Each number appears at least once in each row
for x in range(1,10):
    for z in range(1,10):
        line=""
        for y in range(1,10):
            index_string=str(x)+str(y)+str(z)
            index_int=int(index_string)
            line= line+str(a[index_int])+" "
        line =line+"0"
        f.write(line+"\n")
#Each number appears atmost once in each column
for y in range (1,10):
    for z in range(1,10):
        for x in range(1,9):
            for i in range(x+1,10):
                index_string_1 = str(x)+str(y)+str(z)
                index_string_2 = str(i)+str(y)+str(z)
                index_int_1 = int(index_string_1)
                index_int_2 = int(index_string_2)
                line="-"+str(a[index_int_1])+" -"+str(a[index_int_2])+" 0"
                f.write(line+"\n")
#Each number appears at least once in each column
for y in range(1,10):
    for z in range(1,10):
        line=""
        for x in range(1,10):
            index_string=str(x)+str(y)+str(z)
            index_int=int(index_string)
            line=line+str(a[index_int])+" "
        line=line+"0"
        f.write(line+"\n")
#Each number appears atmost once in a subgrid
for z in range(1,10):
    for i in range(0,3):
        for j in range(0,3):
            for x in range(1,4):
                for y in range(1,4):
                    for k in range(y+1,4):
                        index_string_1=str(3*i+x)+str(3*j+y)+str(z)
                        index_string_2=str(3*i+x)+str(3*j+k)+str(z)
                        index_int_1=int(index_string_1)
                        index_int_2=int(index_string_2)
                        line = "-" + str(a[index_int_1]) + " -" + str(a[index_int_2]) + " 0"
                        f.write(line+"\n")
for z in range(1,10):
    for i in range(0,3):
        for j in range(0,3):
            for x in range(1,4):
                for y in range(1,4):
                    for k in range(x+1,4):
                        for l in range(1,4):
                            index_string_1=str(3*i+x)+str(3*j+y)+str(z)
                            index_string_2=str(3*i+k)+str(3*j+l)+str(z)
                            index_int_1 = int(index_string_1)
                            index_int_2 = int(index_string_2)
                            line = "-" + str(a[index_int_1]) + " -" + str(a[index_int_2]) + " 0"
                            f.write(line+"\n")
#Each number appears atleast once in each subgrid
for z in range(1,10):
    for i in range(0,3):
        for j in range(0,3):
            line = ""
            for x in range(1,4):
                for y in range(1,4):
                    index_string = str(3*i+x)+str(3*j+y)+str(z)
                    index_int=int(index_string)
                    line = line+str(a[index_int])+" "
            line=line+"0"
            f.write(line+"\n")
#Reading the input
inputFile = os.path.abspath(os.path.join(os.getcwd(),'sudoku_inp.txt'))
fin = open(inputFile,"r")
counter_i=1
index_list=[]
while True:
    line = fin.readline()
    if len(line)==0:
        break
    line_components=line.split()
    counter_j = 0
    for item in line_components:
        counter_j=counter_j+1
        if int(item)!=0:
            index_string=str(counter_i)+str(counter_j)+item
            index_int=int(index_string)
            index_list.append(index_int)
    counter_i=counter_i+1
fin.close()
for item in index_list:
    line = str(a[item])+" 0\n"
    f.write(line)
f.close()
#calling Minisat to solve
clauseFile = os.path.abspath(os.path.join(os.getcwd(),'sudoku_dimacs.cnf'))
outputFile = os.path.abspath(os.path.join(os.getcwd(),'sudoku_out.txt'))
p = Popen(['minisat.exe', clauseFile,outputFile], stdin=PIPE, stdout=PIPE, stderr=PIPE)
p.communicate()
fout = open(outputFile,"r")
line=fout.readlines()
line_components=line[1].split()
output_list=[]
for i in line_components:
    val = int(i)
    if (val<0):
        continue
    else:
        for index, variable in a.items():
            if variable == val:
                temp=str(index)
                output_list.append(int(temp[2]))

fout.close()
print(output_list)
solnFile = os.path.abspath(os.path.join(os.getcwd(),'sudoku_soln.txt'))
f_final = open(solnFile,"w")
counter_9 = 1
line=""
for i in output_list:
    line = line+str(i)+" "
    counter_9=counter_9+1
    if counter_9==10:
        f_final.write(line)
        f_final.write("\n")
        line=""
        counter_9=1
f_final.close()