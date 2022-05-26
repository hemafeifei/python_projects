import asyncio, time, threading


async def zusehanshu():  # 测试的阻塞函数
    while True:
        await asyncio.sleep(3)
        threadmingzi()


def threadmingzi():  # 查看当前线程名字
    print("当前线程名字：", threading.current_thread())


def startloop(loop):  # 新建event-loop
    # threadmingzi()  # 看一下线程名字
    asyncio.set_event_loop(loop)
    loop.run_forever()

threadmingzi()
time.sleep(4)
xinjianloop = asyncio.new_event_loop()
threading.Thread(target=startloop, args=(xinjianloop,)).start()
asyncio.run_coroutine_threadsafe(zusehanshu(), xinjianloop)
threadmingzi()

# def main():
#     threadmingzi()
#     time.sleep(4)
#     xinjianloop = asyncio.new_event_loop()
#     threading.Thread(target=startloop, args=(xinjianloop,)).start()
#     asyncio.run_coroutine_threadsafe(zusehanshu(), xinjianloop)
#     threadmingzi()
#
# if __name__ == '__main__':
#     main()