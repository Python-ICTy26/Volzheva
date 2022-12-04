import requests
from bs4 import BeautifulSoup


def extract_news(page):
    """ Extract news from a given web page """
    def get_int(string: str, default: int = 0):
        try:
            return int(string)

        except ValueError:
            return default

    news_list = []

    table_news = page.table.findAll('table')[1]
    tr_article = table_news.find('tr', class_='athing')

    while tr_article is not None:
        tr_props = tr_article.find_next_sibling('tr')
        if tr_props is None:
            break

        # Here:
        #   tr_article - info about article
        #   tr_props - article's properties
        # print('article: \n' + str(tr_article))
        # print('props: \n' + str(tr_props))

        try:
            article_title = tr_article.find('span', class_='titleline').find('a').text
            article_author = tr_props.find('a', class_='hnuser').text
            article_likes = get_int(tr_props.find('span', class_='score').text.split(" ")[0])
            article_comments = get_int(tr_props.findAll('a')[-1].text.replace(u'\xa0', u' ').split(" ")[0])
            article_url = tr_article.findAll('a', href=True)[1]['href']

            news_list.append({
                'author': article_author,
                'comments': article_comments,
                'points': article_likes,
                'title': article_title,
                'url': article_url
            })

        except Exception as e:
            # print(e)
            pass

        # print('----------------------------')
        tr_article = tr_props.find_next_sibling('tr', class_='athing')

    # for item in news_list:
    #     print(item)

    return news_list


def extract_next_page(page):
    """ Extract next page URL """
    try:
        ref = page.table.findAll('table')[1].findAll('td', class_= 'title')[-1].find('a', href=True)['href']
        return ref
    except Exception:
        return ""


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

print(get_news("https://news.ycombinator.com/", 3))
