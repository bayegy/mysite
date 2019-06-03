from journals.nature import Nature
from journals.cell import Cell
from journals.gut import Gut
from journals.microbiome import Microbiome
from journals.science import Science
import time
import threading
from multiprocessing import Pool
import json


class Update(object):
    """docstring for Update"""

    def __init__(self, journal_tribes=False):
        self.journal_tribes = journal_tribes or [[Nature], [Cell], [Gut, Microbiome, Science]]

    def update(self, journal_tribe, time_wait=0, tid=0):
        print("journal tribe {} updator{} is sleeping ({} min)....".format(str(journal_tribe), tid, time_wait))
        time.sleep(time_wait * 60)
        print("journal tribe {} updator{} start to loop update one time each day....".format(str(journal_tribe), tid))
        while True:
            start_time = time.time()
            for journal in journal_tribe:
                # print(str(journal))
                try:
                    journal().update_siblings_db_papers(journal)
                    # n.net.close()
                except Exception as e:
                    print(e)
                    print("Error happened at: " + str(journal))
            end_time = time.time()
            time_used = end_time - start_time
            print("journal tribe {} updator{} done for today, time used: {} min; time now: {}".format(str(journal_tribe), tid, str(time_used / 60),
                                                                                                      time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))

            print("journal tribe {} updator{} is sleeping (one day)....".format(str(journal_tribe), tid))
            time.sleep(3600 * 24 - time_used)

    def multi_thread_update(self, journal_tribe, time_adjust=(0,)):
        for n, t in enumerate(time_adjust):
            td = threading.Thread(target=self.update, args=(journal_tribe, t, n))
            td.start()

    def multi_process_update(self, time_adjust=(0,), cores=False):
        p = Pool(cores or len(self.journal_tribes))
        for journal_tribe in self.journal_tribes:
            p.apply_async(self.multi_thread_update, args=(journal_tribe, time_adjust,))

    def multi_process_update_wild(self, time_adjust=(0,), cores=False):
        """
        This method is weird, but it works for script.
        """
        journal_tribes = self.journal_tribes
        journal_tribe0 = journal_tribes[0]
        del journal_tribes[0]
        self.multi_thread_update(journal_tribe0, time_adjust)
        p = Pool(cores or len(journal_tribes))
        for journal_tribe in journal_tribes:
            p.apply_async(self.multi_thread_update, args=(journal_tribe, time_adjust,))


if __name__ == '__main__':
    import sys
    import re
    ta = re.split(',', sys.argv[1])
    ta = tuple([int(i) for i in ta])
    u = Update()
    u.multi_process_update_wild(ta)
