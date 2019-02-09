'''
## Program: sanity.py
## Authors: Arnav Sharma
##
## Date: 19-01-2019
'''

import sys

from scommands import run_cmd
from sbrowser import stage1, stage3
from serror import *

''' Declare global variables here'''
S1 = False
S2 = False
S3 = False
RID = ""
URL = ""
VERBOSE = False
HELP = False

def shelp():
    """Do sanity tests of a device and update on SCM portal.

  python sanity.py [-s1|-S1] [-s3|-S3] [-rid=RID] [-url=URL] [-v|-V|--verbose]
      [-h|-H|--help|/?]

  -s1 | -S1      Do stage 1 update on SCM Portal.
  -s3 | -S3      Do stage 3 update on SCM Portal.
  -rid=RID       Specify a numeric RID for stage 1 and stage 3 updates. This
                 value must be specified for doing stage 1 and stage 2 updates
                 on SCM portal (i.e. when -s1 or -s2 is used).
  -url=URL       Specify the URL of SCM portal. RID will be concatenated at the
                 end by the program. Default value is (RID obtained from user):
                 http://107.109.51.176:8081/scmportal/
                                        editDeltaMergeUpstreamRequest?id=RID
                 This field will be simply ignored if -s1 or -s2 is not used.
  -v | -V        Show output in detail.
  -h | -H | /?   Display this help.

Options specified multiple times will be ignored."""
    pass    

def set_options():
    """ Set global variables based on user input."""

    global S1
    global S2
    global S3
    global RID
    global URL
    global VERBOSE
    global HELP

    error = False
    args = sys.argv[1:]

    for arg in args:
        if arg == "-s1" or arg == "-S1":
            S1 = True
        elif arg == "-s2" or arg == "-S2":
            S2 = True
        elif arg == "-s3" or arg == "-S3":
            S3 = True
        elif arg[:5] == "-rid=":
            RID = arg[5:]
            if not RID.isdigit():
                set_error("ERR_RID")
                error = True
        elif arg[:5] == "-url=":
            URL = arg[5:]
        elif (arg == "-v") or (arg == "-V") or (arg == "--verbose"):
            VERBOSE = True
        elif arg == "-h" or arg == "-H" or arg == "--help" or arg == "/?":
            HELP = True
        else:
            set_error("ERR_WRONG_OPTION")
            error = True

    if (S1 or S3) and (not RID):
        set_error("ERR_RID")
        error = True
        
    return error

def main():
    """ Start execution here."""

    error = set_options()
    if error:
        print_error()
        return

    if HELP:
        print(shelp.__doc__)
        return

    if not (S1 or S2):
        if VERBOSE:
            print("--- Running sanity tests...")   
        flag_error, flag_issue = run_cmd(VERBOSE)
        
        if flag_error:
            print("--- Program terminated due to errors.")
            if VERBOSE:
                raw_input("Press Enter to exit...")
            return
        
        if flag_issue:
            print("--- Issues were found. Results not posted.")
            if VERBOSE:
                raw_input("Press Enter to exit...")
            return
            
        if VERBOSE:
            print("--- Tests were successful.")

    if S1:
        if VERBOSE:
            print("--- Updating Stage 1 results on portal...")
        flag_error, flag_warn = stage1(RID, URL)
        if VERBOSE:
            if flag_warn:
                print_error()
        if flag_error:
            print("--- Program will terminate due to errors.")
            if VERBOSE:
                raw_input("Press Enter to exit...")
            return

    if S3:
        if VERBOSE:
            print("--- Updating Stage 3 results on portal...")
        flag_error, flag_warn = stage3(RID, URL)
        if VERBOSE:
            if flag_warn:
                print_error()
        if flag_error:
            print("--- Program will terminate due to errors.")
            if VERBOSE:
                raw_input("Press Enter to exit...")
            return

main()
