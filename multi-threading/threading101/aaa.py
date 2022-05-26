import time
import threading

def doWaiting():
    n = 0
    while n < 10:
        print('t1 start waiting {}:'.format(n), time.strftime('%H:%M:%S'))
        time.sleep(2)
        print('t1 stop waiting {}'.format(n), time.strftime('%H:%M:%S'))
        n += 1

def doWaiting2():
    n = 0
    while n < 5:
        print('t2 start waiting {}:'.format(n), time.strftime('%H:%M:%S'))
        time.sleep(3)
        print('t2 stop waiting {}'.format(n), time.strftime('%H:%M:%S'))
        n += 1
t = threading.Thread(target=doWaiting)
t.start()

t2 = threading.Thread(target=doWaiting2)
t2.start()

# 确保线程t已经启动
time.sleep(1)
print('start job')
print('end job')