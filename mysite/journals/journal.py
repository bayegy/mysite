from myutils.net import Net
from myutils.translator import Translator
import re
import os
from abc import abstractmethod, ABCMeta
import json
from myutils.mysql import Mysql
import pdb


class Journal(metaclass=ABCMeta):
    """docstring for Journal"""

    def __init__(self, journal_name, net=False):
        self._base = os.path.dirname(os.path.dirname(__file__))
        with open(self._base + '/config/journal_info.conf', 'r', encoding='utf-8') as f:
            self.journals_info = json.load(f)
        self.url = self.journals_info[journal_name]['url']
        self.IF = self.journals_info[journal_name]['IF']
        self.if_ordered = self.journals_info[journal_name]['if_ordered']
        self.journal_name = journal_name
        # self.db = Mysql("localhost", "root", "947366", "wstdb_academic")
        self.db = Mysql("192.168.196.134", "admin1", "123456", "wstdb_academic")
        self.net = net or Net(protocol=re.sub(':.+', '', self.url).strip())
        self.translator = Translator()
        self.host = re.search('://([^/]+)', self.url).group(1)
        self.siblings = [i for i in self.journals_info.keys() if not self.journals_info[i]
                         ['url'].find(self.host) == -1]

    @abstractmethod
    def get_papers_url(self) ->[]:
        pass

    @abstractmethod
    def get_paper_info(self, paper_url: str) ->[]:
        pass

    def get_full_paper_info(self, paper_url: str) ->[]:
        date, title, paper_type, authors, ca_organs = self.get_paper_info(paper_url)
        translated_title = self.translator.translate_paragraph(title) if title else ""
        return [date, title, translated_title, paper_type, authors, ca_organs, self.journal_name, self.IF, self.if_ordered, paper_url]

    def update_db_papers(self):
        try:
            paper_urls = self.get_papers_url()
            done_urls = self.db.select("tb_papers", field="文献网址").values
            for url in paper_urls:
                if url not in done_urls:
                    try:
                        paper_info = self.get_full_paper_info(url)
                        print('日期：{}, 标题：{}'.format(paper_info[0], paper_info[2]))
                        self.db.insert("tb_papers", paper_info)
                    except Exception as e:
                        print(e)
                        print("Please check paper url: {}".format(url))
        except Exception as e:
            print(e)
            print("Please check journal url: {}, journal name: {}".format(self.url, self.journal_name))

    def update_siblings_db_papers(self, child_class):
        """Can this method be implemented in father class? I don't known yet"""
        for sibling in self.siblings:
            try:
                print("Updating " + sibling)
                # pdb.set_trace()
                child_class(sibling, self.net).update_db_papers()
            except Exception as e:
                print(e)
                print('Error happend at: ' + sibling)
