import sys
import time
# for i in reversed(range(100)):
for i in range(100, 0, -10):
    print(str(i) + '%', end='\r')
    sys.stdout.flush()
    time.sleep(1)