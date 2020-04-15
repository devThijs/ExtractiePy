import os.path
from settings import *
default_outputname = 'extracted_def'
#corrects small user mistakes and combines name and extension as output filename
#returns file name and extension
def user_input_preproc(usr_inputname = default_outputname, outputtype_user = '.csv'):
    oftype = '.' + outputtype_user.replace('.', '') #filetype input with or without point are valid

    f_e_l = usr_inputname.find('.') #find and strip fileextension in name if exists and strip
    if f_e_l == 0: #no character name; revert to default name
        return default_outputname, oftype
    if f_e_l != -1 or 0:
        return usr_inputname.strip(usr_inputname[f_e_l:-1]), oftype
    else:   
        return default_outputname, oftype

#checks if file already exists: if it does, tries to find untaken name
#returns a (untaken) filename
def checkDuplicateFilename(outputname = default_outputname, outputtype_processed = '.csv'):
    filename = './' + outputname + outputtype_processed
    if os.path.exists(filename):
        print('a file with name', filename, 'already exists\n')
        n = 0
        while (n <= 10):
            filename = './' + outputname + '-' + n + outputtype_processed
            if os.path.exists(filename):
                n += 1
                print('a file with name', filename, 'already exists\n')
            else:
                break
        print('Using path/filename:', filename, '\n')
    else:
        print('output filename:', filename)
    return filename

#open and or create file, write matrix data
def outputMatrixCSV(dataMatrix = [], filepath = './data/' + (default_outputname + '.csv')):
    if verbose: print("  Writing output to", filepath, "..")
    if len(dataMatrix) == 0:
        print('Please provide a data matrix to output.')
        return 1
    try:
        file = open(filepath, 'wt')
        rowsinmatrix = len(dataMatrix)
        for irow, row in enumerate(dataMatrix):
            itemsinrow = len(list(row))
            for ielem, element in enumerate(row):
                file.write(str(element))
                if ielem < (itemsinrow - 1):
                    file.write(', ')
                elif rowsinmatrix-1 == irow:
                    break
                else:
                    file.write('\n')
        print(' Writing csv complete.\n Filename: ', filepath)
        return 0
    except FileNotFoundError:
        print('File Not accessible')
        return 1
    finally:
        file.close()



# outputMatrixCSV([[1631,4363,12341],[15135,724782,252356]])