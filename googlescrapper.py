
# author : abilash 9/6/2024  swiftsafe internship assignment

import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime
import json
import threading
import os
    

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

    def save(self,dict_data,folder=""):

        filename =  datetime.now().strftime("%Y%m%d-%H%M%S%f")+".txt"
        filename = os.path.join(folder , filename)
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
        print("link for goole is  = ",fullurl)
        response = super().readhtml(fullurl)
        return response

    def get_links(self, search,start="0"):
        data = self.readhtml(search,start)
        results = self.parse_url(data)
        return results


class linkscrapper(googlescrapper):

    def get_target_site_data(self,link):
        one_website = scrapper(link)
        html = one_website.readhtml()
        return html

    def scrap_all(self, urldict, output_folder =""):
        for one in urldict:
            link = one["link"]
            html_of_target_link = self.get_target_site_data(link)
            dict_data = {"data" : html_of_target_link}
            dict_data.update(one)
            self.save(dict_data, folder = output_folder)


def ask_by_cli(query = "", save="", show_incli="", start="0", output_folder=""):
    gscrapper = linkscrapper()
    query = query or  input(" enter a search term > ")
    results = gscrapper.get_links(query,start)
    for index, result in enumerate(results):
        if not  show_incli:
            print(f"{index + 1}. {result['title']}\n{result['link']}\n")

    folder = output_folder or input("to save results type a folder path else press enter > ")
    if folder:
        gscrapper.scrap_all(results,folder)
        print("everything is saved to ",folder)

class autoscrapper(threading.Thread):
    "this is runni9ng in thread for fast processing of scrapping"
    def __init__(self, query, start, output_folder=""):
        super().__init__()
        self.query = query
        self.start_index = start
        self.output_folder= output_folder

    def run(self) -> None:
        ask_by_cli(self.query, save=True, show_incli=True, start = str(self.start_index), output_folder = self.output_folder)


def scrap_maximum(query, max_results = 7, output_folder=""):
        "this is used for running in thread"
        for start in range(6,int(max_results),6):
            scrapper= autoscrapper(query, start, output_folder)
            scrapper.start()


if __name__ == "__main__":
    print("hello to know how to use this script type following 'python this_scriptname.py --help'")
    import argparse
    parser = argparse.ArgumentParser(description="this will search google for query and reads   targets websites url and saves html data in json format ")
    parser.add_argument("-mx", "--max", help = "total search result to scrap")
    parser.add_argument("-q", "--query", help = "automaticaly scraps provided search query without asking")
    parser.add_argument("-p", "--path", help = "path to folder  where files should be saved. ")
    args = parser.parse_args()
    if args.query  and args.max and args.path:
        scrap_maximum(args.query, max_results = args.max, output_folder=args.path)
    else:
        ask_by_cli()

