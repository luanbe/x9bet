from django.core.management.base import BaseCommand, CommandError
import requests
from bs4 import BeautifulSoup
from news.models import Article


class Command(BaseCommand):
    help = "crawl page https://vtv.vn/the-gioi.htm"
    url = "https://vtv.vn/the-gioi.htm"

    def handle(self, *args, **options):
        articles = self.crawl_list()
        if articles:
            articles = self.crawl_url(articles)
            objs = [
                Article(
                    title=e["title"],
                    image_feature=e["image_feature"],
                    url_crawl=e["url_crawl"],
                    description=e["description"],
                    body=e["body"],
                )
                for e in articles
            ]
            Article.objects.bulk_create(objs)

    def crawl_list(self):
        r = requests.get(self.url)
        if r.status_code == 200:
            articles = []
            html_body = r.text
            soup = BeautifulSoup(html_body, "html.parser")
            posts = soup.select("li.tlitem")
            if posts:
                for post in posts:
                    if post.h4:
                        articles.append(
                            dict(
                                title=post.h4.a.text,
                                image_feature=post.img["src"],
                                url_crawl="https://vtv.vn" + post.h4.a["href"],
                                description=post.select_one("p.sapo").text,
                            )
                        )
                return articles

        return None

    def crawl_url(self, articles):
        for article in articles:
            r = requests.get(article["url_crawl"])
            if r.status_code == 200:
                html_body = r.text
                soup = BeautifulSoup(html_body, "html.parser")
                body = soup.select_one("div.noidung")
                if body:
                    article["body"] = body.text
        return articles
