import time
import os

WORK_DIR = os.getcwd() + "/"
P_NAME = WORK_DIR[:-1].split("/")[-1]

def copy_project():
    tot_p_num = 15
    for idx in range(2, tot_p_num + 1):
        p_name = "P" + str(idx)
        try:
            os.remove(p_name)
        except Exception as err:
            print("os.remove(" + p_name + ") : ", err)
        os.makedirs(p_name, exist_ok=True)
        os.system('cp -R ./P1/* ./{}'.format(p_name))

if __name__ == '__main__':
    start_time = time.perf_counter()
    print("start [" + P_NAME + "]>>>>>>>>>>>>>>>>>>")
    copy_project()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))