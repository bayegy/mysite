from net import Net
from translator import Translator
import re
from abc import abstractmethod, ABCMeta
import json
from mysql import Mysql


class Journal(metaclass=ABCMeta):
    """docstring for Journal"""

    def __init__(self, journal_name):
        with open('config/journal_info.conf', 'r', encoding='utf-8') as f:
            self.journals_info = json.load(f)
        self.url = self.journals_info[journal_name]['url']
        self.IF = self.journals_info[journal_name]['IF']
        self.if_ordered = self.journals_info[journal_name]['if_ordered']
        self.journal_name = journal_name
        # self.db = Mysql("localhost", "root", "947366", "wstdb_academic")
        self.db = Mysql("192.168.196.134", "admin1", "123456", "wstdb_academic")
        self.net = Net(protocol=re.sub(':.+', '', self.url).strip())
        self.translator = Translator()

    @abstractmethod
    def get_papers_url(self) ->[]:
        pass

    @abstractmethod
    def get_paper_info(self, paper_url: str) ->[]:
        pass

    def get_full_paper_info(self, paper_url: str) ->[]:
        date, title, paper_type, authors, ca_organs = self.get_paper_info(paper_url)
        translated_title = self.translator.translate(title) if title else ""
        return [date, title, translated_title, paper_type, authors, ca_organs, self.journal_name, self.IF, self.if_ordered, paper_url]

    def update_db_papers(self):
        paper_urls = self.get_papers_url()
        done_urls = self.db.select("tb_papers", field="文献网址").values
        for url in paper_urls:
            if url not in done_urls:
                full_info = self.get_full_paper_info(url)
                if full_info[1]:
                    self.db.insert("tb_papers", full_info)
