import sys
import time

q = "asdasd"
for i in range(10):
    # sys.stdout.write("\r{0}>".format("="*i))
    # sys.stdout.flush()
    print(str(i), end='\r')
    time.sleep(0.5)

import sys
import time
# for i in reversed(range(100)):
for i in range(100, 0, -10):
    print(str(i) + '%', end='\r')
    sys.stdout.flush()
    time.sleep(1)