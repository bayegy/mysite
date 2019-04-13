from nature import Nature
import time
import threading

np = Nature('NATURE')
global nature_journals
nature_journals = [i for i in np.journals_info.keys() if not np.journals_info[i]['url'].find('www.nature.com') == -1]


def update(time_wait):
    global nature_journals
    print("sleeping....")
    time.sleep(time_wait)
    while True:
        start_time = time.time()
        for jn in nature_journals:
            print(jn)
            try:
                n = Nature(jn)
                n.update_db_papers()
                n.net.close()
            except Exception as e:
                print(e)
                print(n.url)
        end_time = time.time()
        time_used = end_time - start_time
        print("time used: {} min; time now: {}".format(str(time_used / 60),
                                                       time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))

        print("sleeping....")
        time.sleep(3600 * 24 - time_used)


t1 = threading.Thread(target=update, args=(int(3.0833 * 3600),))
t2 = threading.Thread(target=update, args=(int(10.0833 * 3600),))

t1.start()
t2.start()
