# ansi escape code testing

import time


c = 0
while c < 10:
    c += 1
    print('\033[1A\033[0K', end='') # erase previous line 
    print('c is now', c)
    
    time.sleep(0.7)
