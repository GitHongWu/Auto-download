import sys
import time

q = "asdasd"
for i in range(10):
    # sys.stdout.write("\r{0}>".format("="*i))
    # sys.stdout.flush()
    print(str(i), end='\r')
    time.sleep(0.5)