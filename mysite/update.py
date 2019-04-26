from journals.nature import Nature
from journals.cell import Cell
import time
import threading
from multiprocessing import Pool
import json


class Update(object):
    """docstring for Update"""

    def __init__(self):
        with open('config/journal_info.conf', 'r', encoding='utf-8') as f:
            self.journals_info = json.load(f)
        nature_journals = [i for i in self.journals_info.keys() if not self.journals_info[i]
                           ['url'].find('www.nature.com') == -1]
        # cp = Cell("CELL")
        cell_journals = [i for i in self.journals_info.keys() if not self.journals_info[i]
                         ['url'].find('www.cell.com') == -1]

        self.update_info = {
            "NATURE": [Nature, nature_journals],
            "CELL": [Cell, cell_journals]
        }

    def update(self, update_key, time_wait=0, tid=0):
        print("{} updator{} is sleeping ({} min)....".format(update_key, tid, time_wait))
        time.sleep(time_wait * 60)
        print("{} updator{} start to loop update one time each day....".format(update_key, tid))
        while True:
            start_time = time.time()
            for jn in self.update_info[update_key][1]:
                print(jn)
                try:
                    n = self.update_info[update_key][0](jn)
                    n.update_db_papers()
                    n.net.close()
                except Exception as e:
                    print(e)
                    print(n.url)
            end_time = time.time()
            time_used = end_time - start_time
            print("{} updator{} done for today, time used: {} min; time now: {}".format(update_key, tid, str(time_used / 60),
                                                                                        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))

            print("{} updator{} is sleeping (one day)....".format(update_key, tid))
            time.sleep(3600 * 24 - time_used)

    def multi_thread_update(self, update_key, time_adjust=(0,)):
        for n, t in enumerate(time_adjust):
            td = threading.Thread(target=self.update, args=(update_key, t, n))
            td.start()

    def multi_process_update(self, time_adjust=(0,), cores=None):
        keys = self.update_info.keys()

        p = Pool(cores if cores else len(keys))
        for key in keys:
            p.apply_async(self.multi_thread_update, args=(key, time_adjust,))

    def multi_process_update_wild(self, time_adjust=(0,), cores=None):
        """
        This method is weird, but it works for script.
        """
        keys = list(self.update_info.keys())
        key0 = keys[0]
        del keys[0]
        self.multi_thread_update(key0, time_adjust)
        p = Pool(cores if cores else len(keys))
        for key in keys:
            p.apply_async(self.multi_thread_update, args=(key, time_adjust,))


if __name__ == '__main__':
    import sys
    import re
    ta = re.split(',', sys.argv[1])
    ta = tuple([int(i) for i in ta])
    u = Update()
    u.multi_process_update_wild(ta)
