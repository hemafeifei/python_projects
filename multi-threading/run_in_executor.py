from concurrent.futures import ThreadPoolExecutor
import asyncio, time


def zusehanshu():  # 测试的阻塞函数
    while True:
        time.sleep(4)
        threadmingzi()
        return "after 4s"


async def returnfuture():  # 测试新建线程
    loop = asyncio.get_event_loop()
    newexecutor = ThreadPoolExecutor()
    future = await loop.run_in_executor(newexecutor, zusehanshu)  # 执行阻塞函数
    print(future)


def threadmingzi():  # 查看当前线程名字
    import threading
    print("当前线程名字：", threading.current_thread())


asyncio.run(returnfuture())