#This is a tool for extracting specific columns in an arbitrarily terminated string list.
#Specify the termination characters, input and output files, and output filetype

#return all indices of searched string, with the last element being the row termination location


import sys
import file_operations as IO
from enum import Enum
from dataclasses import dataclass



#searches for a specified substring in a provided string
#returns substring start ID
#does not check '-' terminations
def search_string(input_str, search_str, length=0):
    l1 = []
    index = 0
    if length == 0:
        length = len(input_str)
    while index <= length:
        i = input_str.find(search_str, index)
        if i == -1:
            return l1
        l1.append(i)
        # print(l1)
        index = i + 1
    return l1   


#appends a new row of elements[list] to a matrix
def appendNewRowMatrix(matrixname, data = []): 
    matrixname.append( [data[y] for y in range(len(data))] )
        

#returns all strings/elements in a filename as matrix [rows][columns]
def extract(txtfilename, element_termination, row_termination, elementStorageMatrix = []):        
    n=0
    raw = ''
    rawIO = open(txtfilename, 'rt')
    raw = rawIO.read()
    rawIO.close()
    stringlist = []
    row_terminations = search_string(raw, row_termination)  #inventarise all row terminations
    totallines = len(row_terminations) +1

    for row in range(totallines):

        if row==0:
            row_string = raw[0 : row_terminations[row]]
            stringterms = search_string(row_string , element_termination, len(row_string))#inventarise all string terminations in row
        elif row == totallines-1:
            row_string = raw[( row_terminations[row-1]+len(row_termination) ) : len(raw)]
            stringterms = search_string(row_string, element_termination)#inventarise all string terminations in row
        else:
            row_string = raw[( row_terminations[row-1]+len(row_termination) ): row_terminations[row]]
            stringterms = search_string(row_string, element_termination, len(row_string))#inventarise all string terminations in row

        #extract strings from row
        totalstrings = len(stringterms)+1

        for n in range(totalstrings):

            if n==0:    #if first string
                if row==0:#iof first row
                        string = raw[0 : stringterms[n]]
                        stringlist.append(string)
                else:#of last row
                    stringstart = row_terminations[row-1] + len(row_termination)
                    stringend =  stringterms[0] + stringstart
                    string = raw[stringstart : stringend]
                    stringlist.append(string)

            elif n==totalstrings-1:   #if last string
                if row==0:  #of first row
                    stringstart = stringterms[n-1] + len(row_termination)
                    string = raw[stringstart : row_terminations[0] ]
                    stringlist.append(string)
                elif row == totallines-1: #of last row
                    stringstart = row_terminations[row-1] + stringterms[n-1] + len(row_termination) + len(element_termination)
                    string = raw[stringstart:]
                    stringlist.append(string)
                else:
                    stringstart = row_terminations[row-1] + stringterms[n-1] + len(row_termination) + len(element_termination)
                    string = raw[stringstart : row_terminations[row] ]
                    stringlist.append(string )

            else: #all other strings, middle
                stringstart = row_terminations[row-1] + stringterms[n-1] + len(row_termination) + len(element_termination)
                string = raw[ stringstart : stringterms[n] + row_terminations[row-1] + len(row_termination) ]
                stringlist.append(string)

            n+=1

        appendNewRowMatrix(elementStorageMatrix, stringlist)    
        stringlist.clear()

#further processing
#exclude any rows not specified. 
def derive_rows(data = [], include_rows = []): #pass data to process a list of which row id's you want to include in final matrix
    list = []
    matrix = []
    n=0
    include_rows.sort()

    for row in data:
        print(row)
        for i, element in enumerate(row):
            print(element)
            if i== include_rows[n]:
                print('appendlist')
                list.append(element)
                print('list is:', list)
                n += 1
        n=0
        
        appendNewRowMatrix(matrix, list)
        print('matrix:', matrix)
        list.clear()


def checknextarg(first_arg):
    pIndex = sys.argv.index(first_arg)

    try:
        narg = sys.argv[pIndex+1] #test if next element exists
        if '-' not in narg:
            return
            
    except ValueError:
        print('No parameter after' + first_arg)
        print(terminal_instructions)
        return 1

elementStorageMatrixxxx = []
extract('filename.txt', '_', '\n', elementStorageMatrixxxx)
print(elementStorageMatrixxxx[0][0])
print(elementStorageMatrixxxx[1][1])
IO.outputMatrixCSV(elementStorageMatrixxxx)

scriptname = 'stringfind.py' 
terminal_instructions = 'usage: python ' + scriptname + ' -i <inputFilename> -t <element termination> <row termination> (optional: -o <outputFilename>)'


# #when parameter tags are passed in terminal, raise appropriate flag in usrparameters
# #/////////////////////////////////////
# #-------------------------------------
# @dataclass
# class Usrprm:
#     inputP: bool = False
#     terminationP: bool = False
#     extractP: bool = False
#     outputP: bool = False
# #-------------------------------------
# pIndex=0
# if '-i' or '--input' not in sys.argv:
#     print("file input is mandatory")
#     print(terminal_instructions)
#     exit()
# if '-' in (sys.argv.index('-i')+1):
#     if checknextarg('--termination')==1:

#         exit()
# #-------------------------------------
# if '-t'  in sys.argv:
#     if checknextarg('-t')==1:
#         exit()
#     Usrprm.terminationP=True
# elif '--termination' in sys.argv:
#     if checknextarg('--termination')==1:
#         exit()
#     Usrprm.terminationP=True
# if '-e' in sys.argv:
#     if checknextarg('-e')==1:
#         exit()
#     Usrprm.extractP=True
# elif '--extract' in sys.argv:
#     if checknextarg('--extract')==1:
#         exit()
#     Usrprm.extractP=True
# if '-o' in sys.argv:
#     if checknextarg('-o')==1:
#         exit()
#     Usrprm.outputP=True
# elif '--output' in sys.argv:
#     if checknextarg('--output')==1:
#         exit()
#     Usrprm.outputP=True
# #-------------------------------------
# #/////////////////////////////////////