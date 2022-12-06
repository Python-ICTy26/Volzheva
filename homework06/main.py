import scraputils
import db
import hackernews


#
#
COLLECTION_SIZE = 1500


#
#
def load_news():
    news = scraputils.get_news("https://news.ycombinator.com/", int(COLLECTION_SIZE / 30))
    print(news)

    db.clear_db()
    s = db.session()
    for each in news:
        each = db.News(title=str(each['title']),
                       author=str(each['author']),
                       url=str(each['url']),
                       comments=str(each['comments']),
                       points=str(each['points']))
        s.add(each)

    s.commit()


#
#
def run_web():
    hackernews.web_server()


#
#
def main():
    # load_news()
    # run_web()
    pass


if __name__ == "__main__":
    main()
