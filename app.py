import requests
from lxml import html
import csv
from urllib.parse import urljoin

def get(list_elements):
    try:
        return list_elements.pop(0)
    except:
        return ''




scrape_quotes = []

def write_to_csv(data):
    headers = ['text', 'author', 'tags']
    with open('quotes.csv', 'w', encoding="utf-8") as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerows(data)
def scraping(url):
    resp = requests.get(url=url, headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61'
        })

    tree = html.fromstring(html=resp.content)

    quotes = tree.xpath("//div[@class='row']/div/div")

    for quote in quotes:
        q = {

        'text':get(quote.xpath(".//span[@class='text']/text()")),
        'author':get(quote.xpath(".//small[@class='author']/text()")),
        'tags': ' | '.join(quote.xpath(".//div[@class='tags']/a/text()"))
                }
        scrape_quotes.append(q)
    next_page = tree.xpath("//ul[@class='pager']/li/a[contains(text(),'Next')]/@href")

    if len(next_page) != 0:
        next_page_url = urljoin(base=url , url=next_page[0])
        scraping(url=next_page_url)

scraping(url='http://quotes.toscrape.com/')


        

print(len(scrape_quotes))
    
write_to_csv(scrape_quotes)