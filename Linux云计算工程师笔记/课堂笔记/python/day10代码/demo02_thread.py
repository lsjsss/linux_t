import time
import threading
# thread: 线程  ->  threading
def say_hi(seconds):
    print("开始干活~")
    time.sleep(seconds)
    print("干完啦~")
if __name__ == '__main__':
    for i in range(3):
        # 创建新线程, target: 线程分配的任务
        t = threading.Thread(target=say_hi,
                             args=(3, ))
        t.start()  # 线程开始执行任务


# if __name__ == '__main__':
#     for i in range(3):
#         say_hi()
