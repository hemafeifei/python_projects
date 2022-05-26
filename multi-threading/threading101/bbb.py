import time
import threading


class Client(object):
    def __init__(self, name, age, sub_thread=None, conn=None,):
        self.name = name
        self.age = age
        self.conn = conn
        self.sub_thread = sub_thread

    def ping(self):
        n = 0
        while n < 10:
            print('start ping {}:'.format(n), time.strftime('%H:%M:%S'))
            time.sleep(2)
            n += 1

            if self.conn == 0:
                break

    def _connect(self, n=10):
        self.age = self.age + n
        print("New age is {} \n".format(self.age))
        self.conn = 1

    def initial(self):

        self._connect()

        t1 = threading.Thread(target=self.ping)
        # t1.start()
        if self.conn == 1:
            t1.start()
            self.sub_thread = t1
        elif self.conn == 0:
            t1.join()
        return t1



    def other(self):
        time.sleep(4)
        print("[INFO:]datetime is ", time.strftime('%H:%M:%S'))


    def close(self, thread):
        self.conn = 0
        # thread.join()



