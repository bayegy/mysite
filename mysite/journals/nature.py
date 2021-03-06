from lxml import html
from journals.journal import Journal
import re


class Nature(Journal):
    """docstring for Nature"""

    def __init__(self, journal_name=False, net=False):
        super(Nature, self).__init__(journal_name or "NATURE", net)

    def get_papers_url(self):
        tree = self.net.lrequests(self.url, method="get")
        ids = tree.xpath('//a/@href')
        a = ['https://www.nature.com' + i for i in ids if i.startswith('/articles')]
        b = [i for i in ids if re.search('https?://www\.nature\.com/articles', i)]
        return list(set(a + b))

    def get_paper_info(self, paper_url: str):
        tree = self.net.lrequests(paper_url, method="get")
        date = tree.xpath('//time[@itemprop="datePublished"]/@datetime')
        if date:
            date = date[0]
        else:
            date = tree.xpath('//time[@itemprop="datePublished"]/text()')
            date = self.translator.translate_date(date[0])

        title = tree.xpath('//h1/text()')
        title = ''.join(title).strip() if title else ""

        paper_type = tree.xpath('//p[@data-test="article-identifier"]/text()')
        if paper_type:
            paper_type = ''.join(paper_type).strip()
        else:
            paper_type = tree.xpath('//div[@class="article__type"]/text()')
            paper_type = ''.join(paper_type).strip() if paper_type else ""

        authors = tree.xpath('//span[@itemprop="name"]/a/text()')
        if authors:
            authors = ','.join(authors).strip()
        else:
            na = tree.xpath('//h3[@data-tooltip="Show author information"]/text()')
            na = ','.join([i.strip() for i in na]).strip(',')
            cas = [a.strip(" |&|\n") for a in tree.xpath('//h3[@data-tooltip="Show author information"]/a/text()')]
            authors = (na + ',' + ','.join(cas).strip(',')).strip(',')

        ca_og = []
        li_authors = tree.xpath('//li[@itemprop="author"]')
        for li in li_authors:
            ca = li.xpath('span/a[@class="icon icon-right-top icon-mail-12x9-blue pr15"]/text()')
            if ca:
                organs = li.xpath('sup/span/meta[@itemprop="address"]/@content')
                organs = [re.sub('^.*?grid[^,]*,', '', o, count=1).strip() for o in organs]
                ca_og.append(ca[0] + ': ' + '//'.join(organs))
        if not ca_og:
            ca_og = [i for i in tree.xpath(
                '//div[@class="clear cleared"]/div[@class="align-left"]/div/text()') if self.net.find_name(i, cas)]
        ca_organs = ';'.join(ca_og)

        return [date, title, paper_type, authors, ca_organs]
