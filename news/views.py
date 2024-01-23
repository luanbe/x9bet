from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from .models import Article
from django.template import loader
from django.core.paginator import Paginator


def index(request):
    latest_article_list = Article.objects.order_by("-id").all()
    paginator = Paginator(latest_article_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    template = loader.get_template("blog.html")
    context = {"latest_article_list": page_obj, "page_range": paginator.page_range}
    return HttpResponse(template.render(context, request))


def detail(request, article_id):
    post = Article.objects.filter(id=article_id).first()
    recent_posts = Article.objects.exclude(id=article_id)[:10]
    if not post:
        return HttpResponseNotFound("Not Found!")

    template = loader.get_template("post-details.html")
    context = {"post": post, "recent_posts": recent_posts}
    return HttpResponse(template.render(context, request))
