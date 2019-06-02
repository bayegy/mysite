from lxml import html
from journals.journal import Journal
import re
import numpy as np

class Science(Journal):
    """None"""

    def __init__(self, journal_name=False, net=False):
        super(Science, self).__init__(journal_name or "SCIENCE", net)

    def get_papers_url(self):
        tree = self.net.lrequests(self.url, method="get")
        ids = tree.xpath('//a[@class="highwire-cite-linked-title"]/@href')
        a = ['https://science.sciencemag.org' + i  for i in ids if re.search('^/content', i)]
        b = [i for i in ids if re.search('^https://science.sciencemag.org/content', i)]
        return list(set(a + b))

    def get_paper_info(self, paper_url: str):
        tree = self.net.lrequests(paper_url, method="get")

        title = tree.xpath('//h1/div[@class="highwire-cite-title"]/text()')
        title = ''.join(title).strip()

        paper_type= tree.xpath('//div[@class="overline"]/text()')
        paper_type= ''.join(paper_type).strip()

        date= tree.xpath('//div[@class="meta-line"]/text()')
        date= ''.join(date).strip()
        date = self.translator.translate_date(date.split(':')[0]) if date else ""

        author_nodes = tree.xpath('//ol[@class="contributor-list"]/li')

        affiliations = np.array(tree.xpath('//li[@class="aff"]/address/text()'))

        authors = []
        ca_organs = []
        # breakpoint()
        for node in author_nodes:
            author = node.xpath('span[@class="name"]/text()')
            if author:
                author = author[0]
                authors.append(author)

                if node.xpath('a[@class="xref-corresp"]'):
                    og_index = node.xpath('a[@class="xref-aff"]/sup/text()')
                    og_index = [int(i)-1 for i in og_index]
                    affs = affiliations[og_index].tolist()

                    if affs:
                        ca_organs.append("{}: {}".format(author, '//'.join(affs)))

        authors = '; '.join(authors)
        ca_organs = '; '.join(ca_organs)

        return [date, title, paper_type, authors, ca_organs]

