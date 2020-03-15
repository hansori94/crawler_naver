# References:
# https://github.com/sbomhoo/naver_news_crawling_perfect

# Date created: March 6, 2020
# author: Hannah Lee (hansori94)

import requests
from bs4 import BeautifulSoup
from newspaper import Article
from konlpy.tag import Komoran
# from time import sleep
from tqdm import tqdm
import datetime
from wordcloud import WordCloud


def crawler(n, query, s_date=None, e_date=None):
    """
    returns n number of url's of news articles given a search query [query], sorted by relevance
    """
    page = 1
    num_articles = 0
    url_list = []
    if s_date is not None or e_date is not None:
        s_from = s_date.replace(".","")
        e_to = e_date.replace(".","")

    pbar = tqdm(total=n, initial=num_articles)

    while num_articles < n:
        if s_date is None and e_date is None:
            url = "https://search.naver.com/search.naver?where=news&query=" +\
            query + "&start=" + str(page)
        else:
            url = "https://search.naver.com/search.naver?where=news&query=" + query +\
            "&sort=0&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" +\
            s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)
        request = requests.get(url)
        content = request.content
        soup = BeautifulSoup(content, 'html.parser')
        tags = soup.select('._sp_each_title')
        for t in tags:
            url_list.append(t['href'])
            num_articles += 1
            pbar.update(1)
            if num_articles >= n:
                break
        page += 10
    pbar.close()
    return url_list

def get_text(url):
    """
    Returns the contents of the article given in [url]
    """
    a = Article(url, timeout=1)
    failed = ""
    try:
        a.download()
        a.parse()
        result = a.text
    except:
        failed = url + "\n"
        result = ""
    return result, failed

def parse(text):
    """
    Returns a list of parsed nouns from [text] using Komoran parser
    """
    komoran = Komoran()
    nouns = komoran.nouns(text)
    return nouns

def create_wordcloud(parsed_text, filename, stopwords={}):
    """
    Saves a wordcloud image, excluding stopwords
    """
    wordcloud = WordCloud(
        font_path = 'fonts/nanumgothic-bold.ttf',
        width = 800,
        height = 800,
        background_color="white",
        stopwords = stopwords)

    wordcloud = wordcloud.generate_from_text(parsed_text)

    filename = filename +".png"
    wordcloud.to_file('results/wordclouds/'+filename)

def get_freq(wordlist):
    """
    Returns a frequency dictionary given a list of words
    """
    wordfreq = [wordlist.count(p) for p in wordlist]
    freqdict = dict(list(zip(wordlist,wordfreq)))

    result = [(freqdict[key], key) for key in freqdict]
    result.sort(reverse = True)
    return result

def main(n, query, s_date=None, e_date=None):
    """
    ### Parameters:
    [n] int
        - specifies the number of articles to crawl
    [query] string
        - search query
    [s_date] string
        - in format xxxx.xx.xx, specifying the starting
        year, month and date
    [e_date] string
        - in format xxxx.xx.xx, specifying the ending
        year, month and date

    ### Note:
    n = number of articles in [result] + len(failed_urls)
    """
    # n = input("How many articles?: ")
    # query = input("Input the search query: ")
    # txt = input("filename: ")

    url_list = crawler(int(n), query, s_date, e_date) # creates a list of url's
    result = ""
    failed_urls = []

    # pull newspaper contents from each url
    for u in tqdm(url_list):
        text, failed = get_text(u)
        if len(failed) == 0:
            result = result + text
        else: # failure
            failed_urls.append(failed)

    # saving news article text and failed urls to txt files
    # assumes the folder `results` and its subfolder `failed`
    dt = datetime.datetime.now()
    if s_date is None and e_date is None:
        filename = str(n) + '_'+ query + '_' + dt.strftime("%m%d%y_%H%M")
    else:
        filename = str(n) + '_'+ query + '_' + dt.strftime("%m%d%y_%H%M") +\
                    "_" + s_date + 'to' + e_date

    with open('results/news_text/' + filename + ".txt", "w") as f:
        f.write(result)

    with open('results/failed/fail_' + filename + ".txt", "w") as f:
        for u in failed_urls:
            f.write(u+'\n')

    text = parse(result)

    word_list = get_freq(text)
    with open('results/freq/freq_' + filename + ".txt", "w") as f:
        count = 1
        for w in word_list:
            f.write(str(count) + " " + str(w)+'\n')
            count += 1

    create_wordcloud(" ".join(text), filename)


# To run:
main(3, '페이스북', s_date = "2019.01.01", e_date = "2019.05.01")
main(3, '페이스북')
