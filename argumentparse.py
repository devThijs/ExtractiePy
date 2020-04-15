import getopt, sys
from settings import *


def usage():
    print(terminal_instructions)


#return set of mandatory arguments in order: filein, el_termination, row_termination, fileout
def parseArguments():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:o:e:r:v", ["file=", "output=", 'el_termination=', 'row_temination=',"help", "verbose"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        exit()
    verbose = 0

    #store index locations of arguments in vars, shifted by 1 for debugging. Subtract by 1 for actual index
    fiI=0
    foI=0
    etI=0
    rtI=0
    argumentsparsed=0
    argstobeparsed=4
    index=0
    for o, a in opts:

        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("--file", "-f"):
            fiI=index+1
            argumentsparsed+=1
        elif o in ("-o", "--output"):
            foI=index+1
            argumentsparsed+=1
        elif o in ("--el_termination", "-e"):
            etI=index+1
            argumentsparsed+=1
        elif o in ("--row_termination", "-r"):
            rtI=index+1
            argumentsparsed+=1
        elif o == ("-v"):
            verbose = 1
        else:
            print('---option:', o, 'unhandled--')
            assert False, "unhandled option"
        index+=1
    if argumentsparsed != argstobeparsed:
        if fiI==0:
            print("  Input path and filename are mandatory")
            usage()
            exit()
        if foI==0:
            if verbose: print("  Using default output")
        if etI==0:
            print("  Element termination chars are mandatory:")
            usage()
            exit()
        if rtI==0:
            if verbose: print('  Using default row termination: \\n ')
    arguments = []
    if argumentsparsed==4:
        arguments = [opts[fiI-1][1], opts[etI-1][1], opts[rtI-1][1], opts[foI-1][1]]
    elif argumentsparsed==3:
        arguments = [opts[fiI-1][1], opts[etI-1][1], opts[rtI-1][1]]
    else:
        arguments = [opts[fiI-1][1], opts[etI-1][1]]
    return arguments