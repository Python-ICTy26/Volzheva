from bottle import (
    route, run, template, request, redirect
)
from urllib.parse import parse_qs
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/")
def root():
    redirect("/news")


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    # 4. Сохранить результат в БД
    args = parse_qs(request.query_string)
    s = session()
    s.query(News). \
        filter(News.id == int(args['id'][0])). \
        update({'label': str(args['label'][0])})
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    # 1. Получить данные с новостного сайта
    # 2. Проверить, каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    # 3. Сохранить в БД те новости, которых там нет
    s = session()
    for news in get_news("https://news.ycombinator.com/", 1):
        rows = s.query(News).filter(News.title == news['title']).filter(News.author == news['author']).all()
        if len(rows) == 0:
            each = News(title=str(news['title']),
                        author=str(news['author']),
                        url=str(news['url']),
                        comments=str(news['comments']),
                        points=str(news['points']))
            s.add(each)
            s.commit()

    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


def web_server():
    run(host="localhost", port=8080)


if __name__ == "__main__":
    web_server()
