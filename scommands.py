'''
## File: scommands.py
## Authors: Arnav Sharma
##
## Date: 19-01-2019
'''

import shlex
import subprocess

from serror import *
from sglobals import *

def run_cmd(verbose):
    """ Run the commands in CMD and signal errors or issues, if any."""
    global stdout
    global sdcard
    flag_error = False
    flag_issue = False
        
    for cmd, out in zip(CMD, OUT):        
        # Split the arguments into a list for use in Popen
        args = shlex.split(cmd)
        process = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Returns a tuple containing (stdout, stderr)
        std = process.communicate()

        if verbose:
            print("RUN: " + cmd)
        
        stdout = std[0].decode('UTF-8').strip()
        stderr = std[1].decode('UTF-8').strip()
        if "/mnt/media_rw" in stdout:
            sdcard = stdout.split("mnt/media_rw")[1].split("/")[1].strip()
            print sdcard   
        if stderr: 
            set_error("ERR_COMMANDS")
            if verbose:
                print_error(stderr)
            flag_error = True
            reset_error("ERR_COMMANDS")
        else:
            if out == "*" and stdout:
                if verbose:
                    print("SUCCESS: " + stdout)
            elif out == stdout:
                if verbose:
                    print("SUCCESS: " + stdout)
            else:
                flag_issue = True
                if verbose:
                    print("ISSUE: Unexpected Output")
                
    '''
        if stderr:
            set_error("ERR_COMMANDS")
            if verbose:
                print_error(stderr)
            flag_error = True
            reset_error("ERR_COMMANDS")
        elif not stdout:
            if verbose:
                print("ISSUE: No Output")
            flag_issue = True
        else:
            if out:
                if stdout == out:
                    if verbose:
                        print("SUCCESS: " + stdout)
                else:
                    flag_issue = True
                    if verbose:
                        print("ISSUE: Unexpected Output")
            elif verbose:
                print("SUCCESS: " + stdout)
    '''

        
        
                
                
            
    return flag_error, flag_issue
