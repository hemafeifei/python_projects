from threading101.bbb import *
import datetime

def main():
    c = Client('wangxi', 30)
    t1 = c.initial()
    print(c.name)
    print("===="*5)
    c.other()
    print(datetime.datetime.now())
    print("***Close***")
    c.close(t1)


if __name__ == '__main__':
    main()