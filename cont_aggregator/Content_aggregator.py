import requests
from bs4 import BeautifulSoup
from tkinter import *
import re
import inquirer


class News:
    HEADERS = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                         'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/89.0.4389.90 Safari/537.36 '}

    def __init__(self, name_site, hosts, urls, title_tag, news_class, tag, name_class, news_tag, news_class_name):
        self.name_site = name_site
        self.HOST = hosts
        self.URL = urls
        self.title_tag = title_tag
        self.news_class = news_class
        self.tag = tag
        self.name_class = name_class
        self.news_tag = news_tag
        self.news_class_name = news_class_name

    def get_html(self, url, params=""):
        """This function returns HTTP Status Code"""
        r = requests.get(url, headers=self.HEADERS, params=params)
        if r.status_code // 100 == 4 or r.status_code // 100 == 5:
            print("Sorry, the site is temporarily unavailable. Try to select another language or another news website.")
            exit(r)
        return r

    def scraping(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all(f'{self.title_tag}', class_=self.news_class)
        news = []
        news_link = []

        for item in items[:5]:
            news.append({f'{self.name_site}': item.find(f'{self.tag}', class_=f'{self.name_class}').get_text()})
            if self.name_site in item.find(f'{self.tag}', class_=f'{self.name_class}').find('a').get('href'):
                news_link.append(item.find(f'{self.tag}', class_=f'{self.name_class}').find('a').get('href'))
            else:
                news_link.append(
                    self.HOST + item.find(f'{self.tag}', class_=f'{self.name_class}').find('a').get('href'))

        return news, news_link

    def get_updates(self):
        """"This function gives us the news titles and news content"""
        html = self.get_html(self.URL)
        name_news = self.scraping(html.text)[0]
        link_news = self.scraping(html.text)[1]

        return name_news, self.find_text(link_news)

    def find_text(self, url_news):
        """This function returns the news content"""
        news_list = []

        for url in url_news:
            html_news = self.get_html(url).text
            soup = BeautifulSoup(html_news, 'html.parser')
            text = soup.find_all(f'{self.news_tag}', class_=f'{self.news_class_name}')
            cleaner = re.compile('<.*?>')
            clean_text = re.sub(cleaner, '', str(text))
            news_list.append(clean_text)

        return news_list


shamshyan_com = News("shamshyan.com", "https://shamshyan.com/", "https://shamshyan.com/hy/articles/all/",
                     'div', 'news-block', 'h2', 'forth sylfaen', 'div', 'text')

panarmenian_net = News("panarmenian.net", "https://www.panarmenian.net/", "https://www.panarmenian.net/arm/news/",
                       'div', 'theitem padding_left_5 padding_right_5', 'h2', 'font12', 'div', "article_body font11")

azatutyun_am = News("azatutyun.am", "https://www.azatutyun.am/", "https://www.azatutyun.am/news", 'li',
                    'col-xs-12 col-sm-12 col-md-12 col-lg-12 fui-grid__inner', 'div',
                    "media-block__content media-block__content--h media-block__content--h-xs",
                    "div", "wsw")


def view_news(website):
    root = Tk()
    root.title("News Feed")
    root["bg"] = "grey"
    root.minsize(400, 400)

    def title():
        a = 0
        for text_dict in website.get_updates()[0]:
            def printer(i=a):
                print(website.get_updates()[1][i])

            for key, value in text_dict.items():
                buttons = Button(root, text=f"{value}", command=printer)
                buttons['bg'] = "silver"
                buttons.pack()
                a += 1

    news = Button(root, text=f"{website.name_site}", command=title, background="#555", foreground="#ccc")
    news.pack()
    root.mainloop()
    return news


select_website = [
    inquirer.List("news_website",
                  message="Please, select which website you want to view the news."
                          "If you want to read news in English or Russian, do not choose shamshyan.com!!",
                  choices=[f"{shamshyan_com.name_site}", f"{panarmenian_net.name_site}", f"{azatutyun_am.name_site}"])
]
chosen_website = inquirer.prompt(select_website)

if chosen_website["news_website"] != "shamshyan.com":
    select_lang = [
        inquirer.List("Language",
                      message="Select Language",
                      choices=["Armenian", "Russian", "English"])
    ]
    chosen_lang = inquirer.prompt(select_lang)

    """The user can read news in three languages. 
    (Armenian, Russian , English)"""

    if chosen_lang['Language'] == "Russian":
        if chosen_website["news_website"] == "panarmenian.net":
            panarmenian_net.HOST = "https://www.panarmenian.net/rus/"
            panarmenian_net.URL = "https://www.panarmenian.net/rus/news/"

        if chosen_website["news_website"] == "azatutyun.am":
            azatutyun_am.HOST = "https://rus.azatutyun.am/"
            azatutyun_am.URL = "https://rus.azatutyun.am/z/3282"

    if chosen_lang['Language'] == "English":
        if chosen_website["news_website"] == "panarmenian.net":
            panarmenian_net.HOST = "https://www.panarmenian.net/eng/"
            panarmenian_net.URL = "https://www.panarmenian.net/eng/news//"

        if chosen_website["news_website"] == "azatutyun.am":
            azatutyun_am.HOST = "https://www.azatutyun.am/en"
            azatutyun_am.URL = "https://www.azatutyun.am/z/1089"

list_website = [shamshyan_com, panarmenian_net, azatutyun_am]
for site in list_website:
    if site.name_site == chosen_website["news_website"]:
        view_news(site)

