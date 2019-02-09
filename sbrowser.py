'''
## Program: sbrowser.py
## Authors: Arnav Sharma
##
## Date: 19-01-2019
'''

import time
import shlex
import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException

from serror import *
from sglobals import *

''' Declare global variables here'''
# Error flag
flag_error = False
flag_warn = False

''' Javascript functions and html tag IDs'''
# TGID for calling javascript functions
TGID = "168"
# ID of select element
SELECT_ID = 'flagId'
BLOCKER_ID = 'releaseBlockerId'
# Select Option value
ISSUE = "1"
NO_ISSUE = "0"
YES = "1"
NO = "0"
report_button_id = "saveUpstreamTgReport_report"
submit_button_id = "reportSubmit"

def stage1(rid, url=None):
    """ Do stage1 update on SCM portal; pass the URL of SCM portal in case you
        do not wish to use the default one.

        """

    global flag_error
    global flag_warn
    
    try:     
        # start IE driver
        driver = webdriver.Ie(IE_DRIVER)

        # open SCM portal
        if url:
            scm_url = url + rid
        else:
            scm_url = BASE_URL + rid
            
        driver.get(scm_url)

        try: 
            # check if No Issue is already set
##            link_text = driver.find_element_by_xpath(
##                r'//a[@title="Edit Verification Issue Flag"]/../following-sibling::span[1]/text()').strip()

##            set_error("ERR_COMMANDS")
##            print_error("link_text")
##            flag_error = True
            link_text = "Not Updated"

            if "Not Updated" in link_text:    
                # set No Issue
                
                link = driver.find_element_by_xpath(r'//a[@title="Edit Verification Issue Flag"]')   
                link.click()
                # We can call this script also; it has same effect as clicking the
                # button:
                # driver.execute_script("openVerificationIssueDialog('" + rid +
                # "','" + TGID + "','getVarificationDialogTemplate')")

##                set_error("ERR_COMMANDS")
##                print_error("link_button")

                # change window focus
                main_window_handle = None
                while not main_window_handle:
                    main_window_handle = driver.current_window_handle

                dialog_box_window_handle = None
                while not dialog_box_window_handle:
                    for handle in driver.window_handles:
                        if handle != main_window_handle:
                            dialog_box_window_handle = handle
                            break

                driver.switch_to_window(dialog_box_window_handle)

                # select valid options
                select = Select(driver.find_element_by_id(SELECT_ID))
                select.select_by_value(NO_ISSUE)
                # click the add button
                add = driver.find_element_by_xpath(r'//input[@value="Add"]')
                add.click()

##                set_error("ERR_COMMANDS")
##                print_error("select")
##                
                # get focus back to main window
                driver.switch_to_window(main_window_handle)
                
            elif link_text != "No Issue":
                set_error("WARN_ISSUE_OVERWRITE")
                flag_warn = True
            
            # get model no
            model_input = driver.find_element_by_xpath(r'//input[@id="modelName"]')
            model_no = model_input.get_attribute('value')

##            set_error("ERR_COMMANDS")
##            print_error("model")

            # make report path and name
            report_name = model_no + report_base_name
            report_path = report_base_path + report_name
            report_orig_path = report_base_path + report_base_name

            try:
                report_updated = False
                div_report = driver.find_element_by_xpath(r'//div[@id="reportattach"]')
                if report_name == div_report.get_attribute('title'):
                    report_updated = True
            except:
                report_updated = False
                
            if not report_updated:
                # Command to update report name in PC
                copy_cmd = "copy " + report_orig_path + " " + report_path
                # run command to create new file
                args = shlex.split(copy_cmd)
                process = subprocess.Popen(args, shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                # Returns a tuple containing (stdout, stderr)
                std = process.communicate()
                stdout = std[0].decode('UTF-8').strip()
                stderr = std[1].decode('UTF-8').strip()
                if stderr:
                    set_error("ERR_COPY_REPORT")
                    print_error()
                    flag_error = True
                    return flag_error, flag_warn

                # upload report
                driver.execute_script("uploadReport('" + rid +
                                      "','" + TGID + "')")
                report_button = driver.find_element_by_id(report_button_id)
                report_button.send_keys(report_path)
                submit_button = driver.find_element_by_id(submit_button_id)
                submit_button.click()

        except NoSuchElementException:
            set_error("ERR_PAGE_ACCESS")
            print_error()
            flag_error = True
        finally:
            # kill driver
            driver.quit()
            
    except WebDriverException as msg:
        set_error("ERR_DRIVER")
        print_error(str(msg))
        flag_error = True

    return flag_error, flag_warn

def stage3(rid, url=None):
    """ Do stage3 update on SCM portal; pass the URL of SCM portal in case you
        do not wish to use the default one.

        """

    global flag_error
    global flag_warn
    
    try:     
        # start IE driver
        driver = webdriver.Ie(IE_DRIVER)

        # open SCM portal
        if url:
            scm_url = url + rid
        else:
            scm_url = BASE_URL + rid
            
        driver.get(scm_url)

        # check if button exists
        try:
            edit_button = driver.find_element_by_xpath(r'//a[@title="Update Sanity Issue Flag"]')
            edit_button.click()

            # change window focus
            main_window_handle = None
            while not main_window_handle:
                main_window_handle = driver.current_window_handle

            dialog_box_window_handle = None
            while not dialog_box_window_handle:
                for handle in driver.window_handles:
                    if handle != main_window_handle:
                        dialog_box_window_handle = handle
                        break

            driver.switch_to_window(dialog_box_window_handle)

            try:
                # seelct YES and click Add button
                select = Select(driver.find_element_by_id(SELECT_ID))
                select.select_by_value(YES)
                driver.execute_script("updateSanityFlag()")

                # wait for refresh
                time.sleep(5)
                #driver.manage().timeouts().pageLoadTimeout(10, TimeUnit.SECONDS);

                # Check if No Issue already exists
                try:
                    input_box = driver.find_element_by_xpath(r'//input[@id="desc0"]')
                    desc0 = input_box.get_attribute('value')
                    if "No Issue" != desc0:
                        set_error("ERR_DIFF_ISSUE")
                        print_error(desc0)
                        flag_error = True
                    driver.close()
                except:
                    # write no issue
                    input_box = driver.find_element_by_xpath(r'//input[@id="descriptionId"]')
                    input_box.send_keys("No Issue")
                    # select NO in release blocker
                    select = Select(driver.find_element_by_id(BLOCKER_ID))
                    select.select_by_value(NO)
                    # click add button
                    add = driver.find_element_by_xpath(r'//input[@value="Add"]')
                    add.click()

                    # wait for refresh
                    time.sleep(5)
                    #driver.manage().timeouts().pageLoadTimeout(10, TimeUnit.SECONDS);

                    # click close button
                    close = driver.find_element_by_xpath(r'//input[@value="Close"]')
                    close.click()
                finally:
                    # get focus back to main window
                    driver.switch_to_window(main_window_handle)
                
            except NoSuchElementException:
                set_error("ERR_PAGE_ACCESS")
                print_error()
                flag_error = True
            except TimeoutException:
                set_error("ERR_PAGE_LOAD")
                print_error()
                flag_error = True

        except NoSuchElementException:
            pass
        finally:
            # kill driver
            driver.quit()
            
    except WebDriverException as msg:
        set_error("ERR_DRIVER")
        print_error(str(msg))
        flag_error = True

    return flag_error, flag_warn
