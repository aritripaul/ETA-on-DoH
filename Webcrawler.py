#Author: Aritri Paul
#To execute the code, type the following command in your terminal: python3 Webcrawler.py

import requests
import re
from urllib.parse import urlparse, urljoin, urlsplit, SplitResult
from bs4 import BeautifulSoup
import os

internal_urls = set()

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    print("Scraping %s..."%url)
    url_extension=os.path.splitext(urlparse(url).path)[1]

    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        if(len(internal_urls)>=10):
            break
        href = a_tag.attrs.get("href")
        if href == "" or href is None: # href empty tag
            continue

        if(str(url).endswith("/")):
            url = url[:-1]
        
        if(href and href[0]!='#' and href[0]!='/' and str(href).startswith("http")==False):
            url=url+"/"

        
        parsed_href = urlparse(href)
        
        href_ext = os.path.splitext(parsed_href.path)[1]
        if(str(url).endswith(domain_name)==False):
            if(url_extension and href_ext):
                url=url.rpartition('/')[0]
                
                
        href = urljoin(url, href)
        if(href_ext==".html" or href_ext==""):
            fields = urlsplit(href)._asdict()
            fields['path'] = re.sub(r'/$', '', fields['path']) # remove trailing /
            fields['fragment'] = '' # remove targets within a page
            fields = SplitResult(**fields)
             
            if fields.scheme == 'http':
                httpurl =  fields.geturl()
                httpsurl = httpurl.replace('http:', 'https:', 1)

            else:
                httpsurl=fields.geturl()
                            
            href=httpsurl
            if not is_valid(href):
                # not a valid URL
                continue
            if href in internal_urls:
                # already in the set
                continue
            if domain_name not in href:
                # external link
                continue
            
            urls.add(href)
            internal_urls.add(href)
            
    return urls


def crawl(url):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `internal_urls` global set variables.
    
    """
    if(len(internal_urls)>=10):
        return
    links = get_all_website_links(url)
    for link in links:
        crawl(link)


if __name__ == "__main__":
    crawl("https://www.wireshark.org/docs/wsug_html_chunked")
    f=open("url1.txt",'a')
    for url in internal_urls:
        f.write(url+"\n")
    
    print("----------- url.txt successfully created -------------------")                        
    f.close()
