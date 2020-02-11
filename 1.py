from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import sys
import time
import os
from urllib.parse import urlparse
from colorama import init, Fore
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidArgumentException
init(autoreset=True)  # init colorama, with auto reset


def get_urls():
    urlList = []
    url = input('Please enter url: ')
    while url != "-1":
        urlParts = urlparse(url)
        path = urlParts.path.replace("s", "d")
        # TODO Dont replace 's', replace path.spilt('/')[2]
        urlParts = urlParts._replace(path=path)  # replace url path
        urlList.append(urlParts.geturl())
        url = input('Please enter url: ')
    return urlList


def url_validtion(driver, url):
    try:
        driver.get(url)
        driver.implicitly_wait(10)
        return True
    except InvalidArgumentException:
        print(Fore.RED + "INVALID URL", url)
        return False


def find_dl_btn(driver, btn_id):
    try:
        driver.find_element_by_id(btn_id).click()
        driver.implicitly_wait(10)
        return True
    except NoSuchElementException:
        print(Fore.RED + "CAN NOT FIND ELEMENT: " + btn_id)
        return False


def find_attribute_by_element_id(driver, element_id, attribute):
    try:
        driver.find_element_by_id(element_id).get_attribute(attribute)
        # o = driver.find_element_by_class_name("ui-progressbar-value ui-widget-header ui-corner-left")
        driver.implicitly_wait(10)
        return True
    except NameError:
        print(Fore.RED + 'CAN NOT FIND ATTRIBUTE', ": " + attribute)
        return False


def remove_special_char(file_name):
    special_char = {'!', '?', '|', '/', ':', '！', '？'}
    for char in file_name:
        if char in special_char:
            try:
                index = file_name.index(char)
                file_name = file_name[0: index:] + file_name[index + 1::]
            except ValueError:
                print(Fore.RED + 'REMOVE ' + char + ' ERROR')
    # END For
    return file_name


def get_correct_file_name(elements, old_file_name):
    for e in elements:
        file_name = e.text
        if not "請使用現代化瀏覽器" in file_name:
            # remove special symbols, so can rename later
            file_name = remove_special_char(file_name)

            # combine string before "[中国翻訳]" and after "[Chinese]"
            if "[中国翻訳]" in file_name and "[Chinese]" in file_name:
                delimiter1 = "[中国翻訳]"
                delimiter2 = "[Chinese]"
                p1 = file_name.split(delimiter1)
                p2 = file_name.split(delimiter2)
                return p1[0] + p2[1]
            return file_name
    return old_file_name + "GetNewNameError"


# set timeout until next element not 'None'
def progressbar_timeout(driver, element_id, attribute, wait_time):
    for _ in range(wait_time):  # check progress value if found
        if find_attribute_by_element_id(driver, element_id, attribute) is not 'None':
            # print('found attribute')
            return False
        time.sleep(0.5)
        print(find_attribute_by_element_id(driver, element_id, attribute))
    return True  # find attribute time out


# return True if file not exists, False for file exists
def file_timeout(target_dl_folder_path, old_file_name, wait_time):
    for _ in range(wait_time):
        if os.path.exists(target_dl_folder_path + "\\" + old_file_name + ".zip "):
            return False  # file exists
        time.sleep(0.5)
    return True  # file timeout


def retry_task(url, urlList):
    urlList.insert(0, url)


def main():
    if input('c or d: ') is 'd':
        target_dl_folder_path = r"D:\Temp\H"    # target download folder path
    else:
        target_dl_folder_path = r"C:\Temp"

    timeout = 10

    # chrome_options = Options()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    prefs = {"download.default_directory": target_dl_folder_path}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_experimental_option("detach", True)  # keep brower open
    # chrome_options.add_argument("--headless")  # keep brower close
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    # driver.maximize_window()

    while True:
        urlList = get_urls()

        # START FOR each url in urlList
        for url in urlList:

            # check url not validtion, continue to next url
            if not url_validtion(driver, url):
                continue

            # check download btn if found
            if not find_dl_btn(driver, "dl-button"):
                continue

            print(Fore.CYAN + "Downloading", url + " ... ")
            time.sleep(1)

            if progressbar_timeout(driver, "progressbar", "aria-valuenow", timeout):
                continue

            # START while progessbar
            # TODO progressbar stops downloadning stop, retry
            progressbar_value = '0.000'    # init progressbar
            while progressbar_value != "100":
                progressbar_value = driver.find_element_by_id(
                    "progressbar").get_attribute("aria-valuenow")
                sys.stdout.write("\r{0}".format(
                    str(progressbar_value)[:5] + " %"))
                sys.stdout.flush()
                time.sleep(1)
            print()
            time.sleep(1)
            # END while progessbar

            # old file name
            url_path = urlparse(url).path
            try:
                old_file_name = url_path.split("/")[3]
            except IndexError:
                print(Fore.RED + "GET OLD FILE NAME FROM URL ERROR: ", url)
                continue    # go to next url

            # new file name
            potential_filenames = driver.find_elements_by_class_name(
                "alert-success")
            driver.implicitly_wait(10)
            new_file_name = get_correct_file_name(
                potential_filenames, old_file_name)

            # check if file exists in locol folder
            # NOT exists, 3rd arg represent timeout second*2
            if file_timeout(target_dl_folder_path, old_file_name, timeout):
                print(Fore.RED + "DOWNLOAD FAIL", new_file_name)
                print(Fore.CYAN + "RE-DOWNLOAD ...")
                retry_task(url, urlList)
            else:   # file exists
                # replace file name
                try:
                    os.rename(target_dl_folder_path + "\\" + old_file_name + ".zip ",
                              target_dl_folder_path + "\\" + new_file_name + ".zip")
                except os.error:
                    print(Fore.YELLOW + "CAN NOT RENAME ",
                          old_file_name + " -> " + new_file_name)
                finally:
                    print(Fore.GREEN + 'DOWNLOAD COMPLETE',
                          new_file_name + ".zip")

            # TODO unzip

        # END FOR LOOP urlList
    # END WHILE True

    driver.quit()


if __name__ == '__main__':
    main()


'''
TODO List
1.generate report
2.multiple threads
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
