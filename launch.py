import fileIO as iop
import argumentparse as arg
import stringlist_extract as extr
from settings import *

scriptname = 'launch.py' 
terminal_instructions = 'usage: python ' + scriptname + ' -F <inputFilename> -e <element termination> optional: (-r <row termination> optional: -o <outputFilename>)'
elementStorageMatrixxxx = []
arguments = arg.parseArguments()

if verbose: print("  Arguments:", arguments)
if len(arguments)==2:
    elementStorageMatrixxxx = extr.extract(arguments[0],arguments[1])
else:
    elementStorageMatrixxxx = extr.extract(arguments[0],arguments[1],arguments[2])
if len(arguments)==4:
    outputname = iop.user_input_preproc(arguments[3])
    outputname = iop.checkDuplicateFilename(outputname[0])
    iop.outputMatrixCSV(elementStorageMatrixxxx, outputname)
else:
    iop.outputMatrixCSV(elementStorageMatrixxxx)