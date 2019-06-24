import scrapy
from bs4 import BeautifulSoup

DEPTH = 1


class BlogSpider(scrapy.Spider):
    name = 'idnesSpider'
    allowed_domains = ['idnes.cz']
    # Start web page, start on sitemap to find the actual pages.
    start_urls = ['https://www.idnes.cz/sitemap.xml']

    """Crawler settings."""
    custom_settings = {
        'LOG_FILE': 'results/log.log',
        'USER_AGENT': 'School Spider on www.idnes.com FIT CTU 0.1',
        'ROBOTSTXT_OBEY': True,
        'LOG_STDOUT': True,
        'DOWNLOAD_DELAY': 1,
    }

    def parse(self, response):
        """Method for parse site maps for links."""
        if "sitemap" in response.url:
            to_parse = BeautifulSoup(response.body, 'lxml')
            for i in to_parse.find_all("sitemap"):
                url = i.find("loc").text
                if "type=sitemap" not in url:
                    yield scrapy.Request(response.urljoin(response.urljoin(url)), callback=self.parse)
            for i in to_parse.find_all("url"):
                url = i.find("loc").text

                request = scrapy.Request(response.urljoin(response.urljoin(url)), callback=self.parse1)
                time = i.find("n:publication_date")
                request.meta['time'] = time.text if time else None
                request.meta['d'] = DEPTH
                yield request

    def parse1(self, response):
        """Method for parse the articles and pages and save information to JSON."""

        # depth if greater than 0 take links on page and try to crawl
        d = response.meta["d"]
        title = response.css('title::text').extract_first()
        if title is not None:
            title = title.strip()
        description = response.css('meta[name="description"]::attr(content)').extract_first()
        if description is not None:
            description = description.strip()
        keywords = response.css('meta[name="keywords"]::attr(content)').extract_first()
        og_type = response.css('meta[property="og:type"]::attr(content)').extract_first()
        # times from page
        apt = response.css('meta[property="article:published_time"]::attr(content)').extract_first()
        amt = response.css('meta[property="article:modified_time"]::attr(content)').extract_first()
        vpt = response.css('meta[property="video:published_time"]::attr(content)').extract_first()
        vmt = response.css('meta[property="video:modified_time"]::attr(content)').extract_first()

        category = response.css('div[id="portal"]').css('h2').css('a::attr(href)').extract()
        if len(category) > 0:
            category = category[-1]
        else:
            category = None

        text = response.css('div.bbtext::text').extract()
        text.extend(response.css('div.bbtext').css('p::text').extract())
        text = [i.strip() for i in text if i.strip() != '']

        # try to find the full description (pages are not have same structure
        for i in [('div.art-video', 'div[itemprop="description"]::text'),
                  ('div.art-text', 'div[itemprop="description"]::text'),
                  ('div.art-full', 'div[itemprop="description"]::text'),
                  ('div.art-video', 'p.perex::text'),
                  ('div.art-text', 'p.perex::text'),
                  ('div.art-full', 'p.perex::text')]:

            tmp = response.css(i[0]).css(i[1]).extract_first()
            if tmp is not None:
                tmp = tmp.strip()
            if tmp is not None and description is not None and len(tmp) > len(description):
                description = tmp

        # get authors from page
        authors = []
        tmp = response.css('div.authors').css('span[itemprop="name"]::text').extract()
        if tmp is not None:
            authors.extend(tmp)
        tmp = response.css('p.authors').css('a::text').extract()
        if tmp is not None:
            authors.extend(tmp)

        if (text is not None and len(text) > 0) or (description is not None and len(description) > 0):
            yield {'url': response.url, 'title': title, 'type': og_type, 'keywords': keywords,
                   'description': description, 'category': category, 'authors': authors, 'text': text,
                   'article_time_modified': amt, 'article_time_published': apt, 'video_time_modified': vmt,
                   'video_time_published': vpt, 'sitemap_time': response.meta["time"]}
        # if depth is greater than 0 decrement and gor for link get by idnes down on the page.
        if d > 0:
            d -= 1
            pages = []
            tmp = response.css('div[id="related-list"]').css('a::attr(href)').extract()
            pages.extend(tmp)
            tmp = response.css('div[id="abcnejctenejsi"]').css('a::attr(href)').extract()
            pages.extend(tmp)
            tmp = response.css('div[id="abchlavniz"]').css('a::attr(href)').extract()
            pages.extend(tmp)
            for i in pages:
                request = scrapy.Request(response.urljoin(i), callback=self.parse1)
                request.meta['time'] = None
                request.meta['d'] = d
                yield request
