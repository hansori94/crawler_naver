# crawler_naver
Creates a wordcloud of newspaper articles from NAVER, given a search query



Requirements:
- Anaconda distribution of Python 3.7


To run this program,
1) clone this repository 
2) run `conda env create -f naver_crawler.yml`
3) run `conda activate naver_crawler`
4) open `naver_crawler.py`, change the arguments to main() 
4) run `python naver_crawler.py` 

Example output of 200 news articles of 'LP공사':
![alt text](https://github.com/hansori94/crawler_naver/blob/master/results/wordclouds/200_LP%EA%B3%B5%EC%82%AC_030620_1927.png)




### TODO

1. skip over failed_urls, search for more so that we scrape n articles
2. create directory results & failed, images if doesn't exist already
