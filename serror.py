'''
## Program: serror.py
## Authors: Arnav Sharma
##
## Date: 19-01-2019
'''

import sys

''' All error/warning flags'''
ERR_WRONG_OPTION = False
ERR_RID = False
ERR_COMMANDS = False
ERR_DRIVER = False
ERR_PAGE_ACCESS = False
ERR_COPY_REPORT = False
ERR_DIFF_ISSUE = False
ERR_PAGE_LOAD = False
WARN_ISSUE_OVERWRITE = False

def set_error(err_name):
    """ Set error flags. Call this function before calling print_error()."""
    global ERR_WRONG_OPTION
    global ERR_RID
    global ERR_COMMANDS
    global ERR_DRIVER
    global ERR_PAGE_ACCESS
    global ERR_COPY_REPORT
    global ERR_DIFF_ISSUE
    global ERR_PAGE_LOAD
    global WARNING_ISSUE_OVERWRITE

    if err_name == "ERR_RID":
        ERR_RID = True
    elif err_name == "ERR_WRONG_OPTION":
        ERR_WRONG_OPTION = True
    elif err_name == "ERR_COMMANDS":
        ERR_COMMANDS = True
    elif err_name == "ERR_DRIVER":
        ERR_DRIVER = True
    elif err_name == "ERR_PAGE_ACCESS":
        ERR_PAGE_ACCESS = True
    elif err_name == "ERR_COPY_REPORT":
        ERR_COPY_REPORT = True
    elif err_name == "ERR_DIFF_ISSUE":
        ERR_DIFF_ISSUE = True
    elif err_name == "ERR_PAGE_LOAD":
        ERR_PAGE_LOAD = True
    elif err_name == "WARN_ISSUE_OVERWRITE":
        WARN_ISSUE_OVERWRITE = True

def reset_error(err_name):
    """ Reset error flags to default values."""
    global ERR_WRONG_OPTION
    global ERR_RID
    global ERR_COMMANDS
    global ERR_DRIVER
    global ERR_PAGE_ACCESS
    global ERR_COPY_REPORT
    global ERR_DIFF_ISSUE
    global ERR_PAGE_LOAD
    global WARN_ISSUE_OVERWRITE

    if err_name == "ERR_RID":
        ERR_RID = False
    elif err_name == "ERR_WRONG_OPTION":
        ERR_WRONG_OPTION = False
    elif err_name == "ERR_COMMANDS":
        ERR_COMMANDS = False
    elif err_name == "ERR_DRIVER":
        ERR_DRIVER = False
    elif err_name == "ERR_PAGE_ACCESS":
        ERR_PAGE_ACCESS = False
    elif err_name == "ERR_COPY_REPORT":
        ERR_COPY_REPORT = False
    elif err_name == "ERR_DIFF_ISSUE":
        ERR_DIFF_ISSUE = False
    elif err_name == "ERR_PAGE_LOAD":
        ERR_PAGE_LOAD = False
    elif err_name == "WARN_ISSUE_OVERWRITE":
        WARN_ISSUE_OVERWRITE = False

def print_error(opt_msg=None):
    """ Print error messages corresponding to error flags, with an optional
        message passed by the calling function.

        Always call this function after setting error flags with set_error().
        """
    if ERR_RID:
        sys.stderr.write("ERROR: No/Invalid rid\n")
    elif ERR_WRONG_OPTION:
        sys.stderr.write("ERROR: Wrong option specified\n")
    elif ERR_COMMANDS:
        if opt_msg:
            sys.stderr.write("ERROR: " + opt_msg + "\n")
        else:
            sys.stderr.write("ERROR: Unable to run commands\n")
    elif ERR_DRIVER:
        if opt_msg:
            sys.stderr.write("ERROR: " + opt_msg + "\n")
        else:
            sys.stderr.write("ERROR: WebDriver error\n")
    elif ERR_PAGE_ACCESS:
        sys.stderr.write("ERROR: Unable to access elements in page\n")
    elif ERR_COPY_REPORT:
        sys.stderr.write("ERROR: Report not found / cannot be copied\n")
    elif ERR_DIFF_ISSUE:
        if opt_msg:
            sys.stderr.write("ERROR: Issue already exists - " + opt_msg + "\n")
        else:
            sys.stderr.write("ERROR: Issue already exists\n")
    elif ERR_PAGE_LOAD:
        sys.stderr.write("ERROR: Timeout - Unable to load page\n")
    elif WARN_ISSUE_OVERWRITE:
        sys.stderr.write("Warning: Stage1 Issue already exists, overwrite No Issue\n")
