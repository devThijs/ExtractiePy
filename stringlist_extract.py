#This is a tool for extracting specific columns in an arbitrarily terminated string list.
#I needed a list of hexadecimal values for ASCII characters. Searching for a few minutes(yeah i could have just looked harder lol) 
#I could only find full tables for ASCII, not the specific values i needed; prompting me to write this script
#so as to not have to type the entire table rows myself.

#how to use:
#Specify the termination characters, input and output filename. Currently only supports csv output
#return all indices of searched string, with the last element being the row termination location


import sys
import fileIO as iop
from enum import Enum
from dataclasses import dataclass
from settings import *




#searches for a specified substring in a provided string
#returns substring start ID
#does not check '-' terminations
def search_string(input_str, search_str = '\n', length=0):#string to search within, phrase to search
    l1 = []
    index = 0
    if length == 0:
        length = len(input_str)
    while index <= length:
        i = input_str.find(search_str, index)#return -1 if not found
        if i == -1:
            if verbose==2: print("  Row search exit index:", index)
            return l1
        l1.append(i)
        # print(l1)
        index = i + 1
    return l1   


#appends a new row of elements[list] to a matrix
def appendNewRowMatrix(matrixname, data = []): 
    matrixname.append( [data[y] for y in range(len(data))] )
        

#returns all strings/elements in a filename as matrix [rows][columns]
def extract(txtfilename, element_termination, row_termination = '\n'):
    elementStorageMatrix = []
    n=0
    raw = ''
    rawIO = open(txtfilename, 'rt')
    raw = rawIO.read()
    if verbose==2: print(raw)
    rawIO.close()
    stringlist = []
    row_terminations = search_string(raw, row_termination)  #inventarise all row terminations
    if verbose==2: print('  row termination ids:', row_terminations)
    totallines = len(row_terminations) +1
    if verbose==2: print('  totallines:', totallines)

    if raw == '':
        print("  Yo this file is empty")
        exit()
    stringterms = []
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
        if verbose==2: print("  Elements in", str(row) + "nth", "row:", totalstrings, end='')
        if totalstrings<=1: print(  "Oop somthing went wrong. \n--Please check if your arguments are correct--")
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
    if verbose: print("  Extraction complete.\n  Total rows:", totallines, "\n  Total elements:", totallines*len(elementStorageMatrix[1]))
    return elementStorageMatrix


#further processing
#exclude any columns not specified. Pass data to process column id's you want to include in final matrix
#processes matrix row by row
def derive_columns(data = [], include_columns = []):
    list = []
    matrix = []
    n=0
    include_columns.sort()
    if include_columns==0:
        print("  No columns defined, skipping column derivation.")
    return data
    for row in data:
        # print(row)
        for i, element in enumerate(row):
            # print(element) if verbose==True
            if i== include_columns[n]:
                list.append(element)
                n += 1
            if n == len(include_columns) -1:
                if verbose==2: print('extracted column vals:', list)
                break
        n=0
        
        appendNewRowMatrix(matrix, list)
        if verbose: print('appending to matrix..')
        list.clear()
    if verbose: print(' deriving select columns completed..')
    return matrix


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