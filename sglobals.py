'''
## Program: sglobals.py
## Authors: Arnav Sharma
##
## Date: 19-01-2019
'''

import os
import shlex
import subprocess

''' Declare global variables to be used throughout'''

''' sanity-ui
    '''
APP_TITLE = "Sanity App - File System"

''' scommands.py
    '''
stdout = ""
sdcard = ""
cmd= "adb shell \"df | grep -w '/mnt/media_rw'\""
args = shlex.split(cmd)
process = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
std = process.communicate()
stdout = std[0].decode('UTF-8').strip()
if "/mnt/media_rw" in stdout:
    sdcard = stdout.split("mnt/media_rw")[1].split("/")[1].strip()


### List of all commands to be executed
CMD = [
 "adb shell \"df | grep -w '/data'\"",
 #"adb shell \"df | grep '/mnt/shell/enc_media'\"",
 "adb shell \"mount | grep ' sdcardfs'\"",
 "adb shell \"ls -l | grep 'sdcard -> '\"",
 "adb shell \"ls -l /mnt | grep 'sdcard -> '\"",
 "adb shell echo $EXTERNAL_STORAGE",
 "adb shell \"echo 'Hello' > /storage/emulated/0/test.txt\"",
 "adb shell \"cat /storage/emulated/0/test.txt\"",
 "adb shell \"rm /storage/emulated/0/test.txt\"",
 "adb shell \"ls -A /storage/emulated/0/ | grep -w test.txt\"",
 "adb shell \"df | grep -w '/mnt/media_rw'\"",
 "adb shell \"echo 'Hello' > /storage/"+sdcard+"/test.txt\"",
 "adb shell \"cat /storage/"+sdcard+"/test.txt\"",
 "adb shell \"rm /storage/"+sdcard+"/test.txt\"",
 "adb shell \"ls -A/storage/"+sdcard+"/test.txt 2> /dev/zero | grep -w test.txt\""
 
]

 ### List of expected output corresponding to each command in CMD. Empty string
### means the output is not prespecified.
OUT = [
 "*",
 #"",
 "*",
 "*",
 "*",
 "/sdcard",
 "",
 "Hello",
 "",
 "",
 "*",
 "",
 "Hello",
 "",
 ""
]

''' sbrowser.py
    '''
# Path to IEDriverServer
#IE_DRIVER = r"E:\\tools\\sanity\\utils\\IEDriverServer_x64_2.53.1\\IEDriverServer.exe"
IE_DRIVER = r"C:\\Users\\p.gadia\\Desktop\\sanity-tool\\IEDriverServer_x64_2.53.1\\IEDriverServer.exe"

# SCM Portal base url
BASE_URL = r"http://107.109.51.176:8081/scmportal/editDeltaMergeUpstreamRequest?id="

# Report to be uploaded
report_base_name = "SystemMemory_UpstreamSanityTestCases.xlsx"
report_base_path = os.getcwd() + "\\"
