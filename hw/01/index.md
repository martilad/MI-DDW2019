# HW1 - Data Acquisition - Web Crawler/Scraper
Solution of homework 1.
    
## Task (assignment)

* Select a web source of your own choice for the non-trivial web crawling task.
    * The resource should contain hundreds/thousands of unique pages to crawl.
    * Each page should contain at least:
        * Title - e.g. an article title, a product title, ...
        * Main content/text - a main text of the article, a description of the product, ...
        * Additional features describing the page - information about author, date of publishing, product item parameters, ...
* Identify possible issues with crawling:
    * Explore the robot exclusion protocol, availability of the sitemaps description, ...
    * Identify issues with extraction of relevant information
        * Extraction using machine readable annotations, own set of rules/selectors, automatic detection of the content, ...
* Properly design and implement the extraction task
    * Inputs and outputs of the task
    * Dealing with policies
    * Selection of the language/tools
* Configure the crawler
    * focus on crawling of just one single host (domain)
    *  set the crawl interval! Otherwise you can be banned!
    * set the crawl depth
    * user-agent string
    * seed URLs
    * and other settings you consider important.
    
## Solution

For this domain, I have chosen the idnes.cz media server. 
From the domain I will download the latest articles. 
Additionally, if applicable, members that are current or related.

The site has nicely made sitemaps, 
where the introductory ones serve as a signpost for individual sites (cars, technet, etc ...). 
The sitemaps referenced in the introductory are the articles in the last month with some information.

### Possible issues:

I do not expect any obstacles with crawling. 
Only for future data processing may be an obstacle that data from the Web 
can not be publicly distributed without the consent of MAFRA, a.

### Describe the design:

In my role, I will implement a crawler that will download the latest members and 
possibly the articles to which they refer. 
The number of adjectives on the recommended articles will be possibly specified by some constant.

The Crawler will start at the top of the sitemap to get the latest articles to download and 
save to a JSON file that can be further processed by the machine.

### Implementation:

By default, the initial domain I have chosen is a sitemap and an authorized domain that is idnes.cz. 
I set the interval to 1 second so that I do not load the crawled web. 
I further specified the robots.txt file for the crawler, which is then respected. 
It also set the USER_AGENT string to *School Spider on www.idnes.com FIT CTU 0.1* to identify the robot.

I did not take advantage of the library implementation for the depth of the search, 
but I managed it myself. Depth decreases each time the recommended articles are visited.

While crawler crawl loads sitemaps and articles over the last 7 days, 
I crawl, parse, and save the results to the file. Depending on the depth, 
I also add other recommended articles to crawl.

Filtration of duplicate pages is implemented in the library using the scrapy.dupefilters.RDPDupeFilter class. 
To eliminate duplicates I used this implementation and enabled it in a crawler.

Implementation is in src/crawler.py.
For run the crawler you can use script run.sh. It use Python3.7 and it is need have instaled it.

### Results:

The data is in json format, whose schema is in results/schema.json. 
Every article tries to crawl the following information:
url, title, type, keywords, description, category, authors, text, article_time_modified, 
article_time_published, video_time_modified, video_time_published, sitemap_time.

The data itself is stored in results/data.json
For run I set the depth of search to one.

### Issues during design/extraction:
The biggest problem with the whole crawling was the different structure of individual parts of the site 
(cars, technet, mobile, etc ...). Some of the information was duplicated, 
otherwise only partially, in some of the pages, and often on the other page again and again.

I also met a differently formatted text where I was most surprised by the page:
```
<div class='some'>
    some text
    <p></p>
    some text
    <p></p>
    ...
</div>
```
I have tried to solve this problem even though it is not always ideal for splitting the stalks.