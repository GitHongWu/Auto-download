from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidArgumentException
# from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import sys
import time
import os


def parseUrl():
    urlList = []
    url = input()
    while url != "-1":
        urlParts = urlparse(url)
        path = urlParts.path
        path = path.replace("s", "d")
        urlParts = urlParts._replace(path=path)
        url = urlParts.geturl()
        urlList.append(url)
        url = input()
    return urlList


def get_correct_file_name(elements):
    for e in elements:
        new_file_name = e.text
        if not "請使用現代化瀏覽器" in new_file_name:
            if "[中国翻訳]" in new_file_name and "[Chinese]" in new_file_name:
                delimiter1 = "[中国翻訳]"
                delimiter2 = "[Chinese]"
                p1 = new_file_name.split(delimiter1)
                p2 = new_file_name.split(delimiter2)
                return p1[0] + p2[1]
            return new_file_name
    return "None"
    

def main():
    print("Please enter url: ")
    urlList = parseUrl()
    target_dl_folder_path = r"C:\Temp"
    # target_dl_folder_path = r"D:\Temp\H"    # target download folder path

    # chrome_options = Options()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    prefs = {"download.default_directory" : target_dl_folder_path}
    chrome_options.add_experimental_option('prefs', prefs)
    # chrome_options.add_experimental_option("detach", True)  # keep brower open
    chrome_options.add_argument("--headless") # keep brower close
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    # driver.maximize_window()

    # START FOR each url in urlList
    dl_btn_id = "dl-button"
    for url in urlList:
        try:
            driver.get(url)
            driver.implicitly_wait(10)
        except InvalidArgumentException:
            print("INVALID URL")
            continue

        try:
            driver.find_element_by_id(dl_btn_id).click()
            driver.implicitly_wait(10)
        except NoSuchElementException:
            print("CAN NOT FIND ELEMENT: " + dl_btn_id)
            continue
        finally:
            # driver.implicitly_wait(10)
            pass
        
        print("Downloading " + url + " ... ")
        time.sleep(1)
        try:
            progressbar = driver.find_element_by_id("progressbar").get_attribute("aria-valuenow")
            # o = driver.find_element_by_class_name("ui-progressbar-value ui-widget-header ui-corner-left")
            driver.implicitly_wait(10)
        except NoSuchElementException:
            print("NO PROGRESSBAR")
            continue
        
        # old file name
        url_path = urlparse(url).path
        try:
            old_file_name = url_path.split("/")[3]
        except IndexError:
            print("GET OLD FILE NAME ERROR: ", url)
            continue
        
        # new file name
        potential_filenames = driver.find_elements_by_class_name("alert-success")
        driver.implicitly_wait(10)
        new_file_name = get_correct_file_name(potential_filenames)
        
        # START while progessbar
        while progressbar != "100":
            progressbar = driver.find_element_by_id("progressbar").get_attribute("aria-valuenow")
            sys.stdout.write("\r{0}".format(str(progressbar) + " %"))
            sys.stdout.flush()
            time.sleep(0.5)
        print()
        # END while progessbar

        # STRAT while loop until file appear in folder
        timeout = 10
        while not os.path.exists(target_dl_folder_path + "\\" + old_file_name + ".zip "):
            if i is timeout - 1:
                print("DOWNLOAD FAIL(TIMEOUT): " + new_file_name + ".zip")
                break
            i += 1
            time.sleep(0.5)
        # END while

        # replace file name
        try:
            os.rename(target_dl_folder_path + "\\" + old_file_name + ".zip ", target_dl_folder_path + "\\" + new_file_name + ".zip")
        except os.error:
            print("CAN NOT RENAME ", old_file_name, " -> ", new_file_name)
        
        print("DOWNLOAD COMPLETE: " + new_file_name + ".zip")
        
        # TODO unzip

    # END for urlList

    driver.quit()


if __name__ == '__main__':
    main()


'''
TODO List
1.report
2.multiple tasks
3.GUI
'''

'''
EN
https://b-upp.com/en/s/312266/
https://b-upp.com/en/s/312545/
https://b-upp.com/en/s/312257/
https://b-upp.com/en/s/312465/
-1
'''

'''
CN
https://b-upp.com/cn/s/312429/
https://b-upp.com/cn/s/312287/
https://b-upp.com/cn/s/312287/
'''