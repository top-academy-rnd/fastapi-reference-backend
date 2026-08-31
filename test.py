import threading
from time import sleep

NUMBERS = []


def function_for_thread_2():
    acked_len = 0
    while True:
        if len(NUMBERS) > acked_len:
            print("")
            print("sum: ", sum(NUMBERS))
            print("> ", end="")
            acked_len = len(NUMBERS)
        sleep(5)


th_2 = threading.Thread(target=function_for_thread_2)
th_2.start()


while True:
    NUMBERS.append(int(input("> ")))
