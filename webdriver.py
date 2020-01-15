from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException

url = "https://b-upp.com/cn/d/312429/"
# url = "asd"
driver = webdriver.Chrome()
driver.implicitly_wait(10)
try:
    driver.get(url)
    driver.implicitly_wait(10)
except InvalidArgumentException:
    print("invalid arguement")

# o = driver.find_elements_by_class_name("alert-success").text  # ok
o = driver.find_elements_by_class_name("alert-success")
for element in o:
    string = element.text
    print(string)
    if not "請使用現代化瀏覽器" in string:
        print("correct: " + element.text)
# o = driver.find_elements_by_class_name("alert-success").Text  # NOT
# o = driver.find_elements_by_class_name("alert-success").get_attribute('Text') # NOT   or 'text'   # x
# print(driver.find_element_by_css_selector('div.alert.alert-success').text)  # ok
driver.implicitly_wait(10)
print(o)