from urllib.parse import urlparse

s = "C:\\Temp"
filename = "1233453"
print(s + "\\" + filename + ".zip ")

path="/cn/d/312429/"
p = path.split("/")[2].replace('s', 'd')
for e in p.length():
    print(e)

url = "https://b-upp.com/cn/s/312429/"
# url = "b-upp.com/cn/s/312429/"
# url_path = urlparse(url).path.split("/")[3]
url_path = urlparse(url)
print(url_path)

urlParts = urlparse(url)
path = urlParts.path
path = path.split("/") #[2].replace("s", "d")
print(path)