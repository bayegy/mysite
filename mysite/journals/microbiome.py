from lxml import html
from journals.journal import Journal
import re


class Microbiome(Journal):
    """None"""
    def __init__(self):
        super(Microbiome, self).__init__("Microbiome")

    def get_papers_url(self):
        tree = self.net.lrequests(self.url, method="get")
        ids = tree.xpath('//a[@data-test="title-link"]/@href')
        a = ['https://microbiomejournal.biomedcentral.com' + i for i in ids if re.search('^/articles', i)]
        b = [i for i in ids if re.search('^https://microbiomejournal.biomedcentral.com/articles', i)]
        return list(set(a + b))

    def get_paper_info(self, paper_url: str):
        tree = self.net.lrequests(paper_url, method="get")

        title = tree.xpath('//h1/text()')
        title = ''.join(title).strip() if title else ""

        
        date = tree.xpath('//span[@itemprop="datePublished"]/text()')
        if date:
            date = " ".join(date[0].split())
            date = self.translator.translate_date(date)
        else:
            date = ""

        organ_dict={}
        organ_nodes=tree.xpath('//div[@class="Affiliation"]')
        for node in organ_nodes:
            id = node.xpath('@id')
            id = id[0] if id else ""
            organ = node.xpath('div[@class="AffiliationText"]/text()')
            organ = organ[0] if organ else ""
            # breakpoint()
            if id:
                organ_dict[id.replace('#', '').strip()]=organ

        authors=[]
        ca_organs=[]
        authors_nodes=tree.xpath('//li[@class="Author hasAffil"]')
        for node in authors_nodes:
            author = node.xpath('span[@class="AuthorName"]/text()')
            author = " ".join(author[0].split())  if author else ""
            authors.append(author)
            if node.xpath('a[@class="EmailAuthor"]'):
                ids = node.xpath('sup/a[@class="AffiliationID"]/@href')
                # breakpoint()
                try:
                    organs = [organ_dict[id.replace('#', '').strip()] for id in ids]
                except IndexError:
                    organs = []
                ca_organs.append(author + ": " + "//".join(organs) if organs else "")
        authors = [author for author in authors if author]
        authors = '; '.join(authors)
        ca_organs = [" ".join(organ.split()) for organ in ca_organs if organ]
        ca_organs = '; '.join(ca_organs)

        paper_type=tree.xpath('//li[@data-test="article-category"]/text()')
        paper_type = paper_type[0] if paper_type else ""
        return [date, title, paper_type, authors, ca_organs]



