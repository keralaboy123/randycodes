
# author :keralaboy123 9/6/2024  swiftsafe internship assignment

import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import json

USERAGENT = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0'}

class scrapper:
    def __init__(self,url,headers={}):
        self.url = url
        self.headers = headers or USERAGENT

    def readhtml(self,url="",header = {}):
        url = url or self.url
        header = header or self.headers
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text
        else:
            return ""

    def save(self,dict_data,filename=""):
        filename = filename or time.strftime("%Y%m%d-%H%M%S")+".txt"
        with open(filename,"w+") as file:
            json.dump(dict_data, file, indent = 6)


class googlescrapper(scrapper):
    url = "https://www.google.com/search?q="

    def __init__(self,url=""):
        url = url or self.__class__.url
        super().__init__(url)
    def parse_url(self, htmldata):
        soup = BeautifulSoup(htmldata, 'html.parser')
        search_results = []

        for divtags in soup.find_all('div', class_='yuRUbf'):
            links = divtags.find_all('a', href=True)
            if links:
                link = links[0]['href']
                title = divtags.find('h3').text
                item = {
                    'title': title,
                    'link': link
                }
                search_results.append(item)
        return search_results

    def readhtml(self,query,start="0"):
        query = urllib.parse.quote_plus(query)
        fullurl = self.url + query +"&start="+start
        response = super().readhtml(fullurl)
        return response

    def get_links(self, search):
        data = self.readhtml(search)
        results = self.parse_url(data)
        return results


class linkscrapper(googlescrapper):
    def get_target_site_data(self,link):
        one_website = scrapper(link)
        html = one_website.readhtml()
        return html

    def scrap_all(self,urldict):
        for one in urldict:
            link = one["link"]
            html_of_target_link = self.get_target_site_data(link)
            dict_data = {"data" : html_of_target_link}
            dict_data.update(one)
            self.save(dict_data)


def ask_by_cli(query = "",save="",show_incli=""):
    gscrapper = linkscrapper()
    query = query or  input(" enter a search term > ")
    results = gscrapper.get_links(query)
    for index, result in enumerate(results):
        if  show_incli:
            print(f"{index + 1}. {result['title']}\n{result['link']}\n")

    query = save or input("type anything if you want to save it to file else press enter > ")
    if query:
        gscrapper.scrap_all(results)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auto", help="automaticaly scraps provided search query and shows results in cli")
    parser.add_argument("-sh", "--show", help="show in cli the scrapped urls and titles.type any charecter to turn it on")
    parser.add_argument("-s", "--save", help="automaticaly save's urls scrapped. type any charecter to turn it on ")
    args = parser.parse_args()
    if args.auto :
        ask_by_cli(args.auto,args.save,args.show)
    else:
        ask_by_cli()


