from lxml import html
from journals.journal import Journal
import re


class Gut(Journal):
    """None"""

    def __init__(self, journal_name=False, net=False):
        super(Gut, self).__init__(journal_name or "GUT", net)

    def get_papers_url(self):
        tree = self.net.lrequests(self.url, method="get")
        ids = tree.xpath('//a[@class="highwire-cite-linked-title"]/@href')
        a = ['https://gut.bmj.com' + i + '.info' for i in ids if re.search('^/content/early', i)]
        b = [i + '.info' for i in ids if re.search('^https://gut.bmj.com/content/early', i)]
        return list(set(a + b))

    def get_paper_info(self, paper_url: str):
        tree = self.net.lrequests(paper_url, method="get")

        title = tree.xpath('//cite/div[@class="highwire-cite-title"]/text()')
        title = ''.join(title).strip() if title else ""

        ca_organs = tree.xpath('//li[@class="corresp"]/text()')
        ca_organs = [organ.strip() for organ in ca_organs if organ.strip()]
        ca_organs = '  '.join(ca_organs)

        first_authors = tree.xpath('//li/span[@class="nlm-given-names"]/text()')
        last_authors = tree.xpath('//li/span[@class="nlm-surname"]/text()')
        authors = '; '.join([first + ' ' + last for first, last in zip(first_authors, last_authors)]
                            ) if len(first_authors) == len(last_authors) else '; '.join(last_authors)

        paper_type = tree.xpath('//div[@class="field-item even"]/text()')
        paper_type = [t.strip() for t in paper_type if t.strip()]
        paper_type = paper_type[-1] if paper_type else ""

        date = tree.xpath('//li[@class="published"]/text()')
        date = self.translator.translate_date(''.join(date).strip()) if date else ""
        # breakpoint()
        return [date, title, paper_type, authors, ca_organs]
