from lxml import html
from journals.journal import Journal
import re


class Cell(Journal):
    """
    class to get the paper information of Cell related journals
    """

    def __init__(self, journal_name=False, net=False):
        super(Cell, self).__init__(journal_name or "CELL", net)

    def get_papers_url(self):
        tree = self.net.lrequests(self.url, method="get")
        ids = tree.xpath('//a/@href')
        a = ['https://www.cell.com' + i for i in ids if re.search('^/.*fulltext', i)]
        b = [i for i in ids if re.search('https?://www\.cell\.com.*fulltext', i)]
        return list(set(a + b))

    def get_paper_info(self, paper_url: str):
        tree = self.net.lrequests(paper_url, method="get")

        date = tree.xpath('//span[@class="article-header__publish-date__value"]/text()')
        if date:
            date = date[0]
        else:
            date = tree.xpath('//div[@class="article-info__date"]/text()')
            date = date[0] if date else ""

        date = date.replace('online', '').replace('Published', '').replace(':', '').replace('：', '')

        date = self.translator.translate_date(date) if date else ""

        title = tree.xpath('//h1/text()')
        title = ''.join(title).strip() if title else ""

        paper_type = tree.xpath('//span[@class="article-header__journal"]/text()')
        paper_type = paper_type[0] if paper_type else ""

        authors_tree = tree.xpath('//li[@class="loa__item author"]')
        authors = []
        ca_organs = []
        for tr in authors_tree:
            author = tr.xpath('*/a/text()')
            author = author[0].strip() if author else ""
            authors.append(author)
            if tr.xpath('*/*/i[@class="icon-Email faded"]'):
                org = tr.xpath('*/*/*/*/*/div/text()')
                org = [o.strip() for o in org]
                ca_organs.append(author + ': ' + '//'.join(org))

        authors = ','.join(authors)
        ca_organs = ';'.join(ca_organs)

        return [date, title, paper_type, authors, ca_organs]
