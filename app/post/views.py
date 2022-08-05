from app.models import Articles
from flask import render_template

from . import post


@post.route("/")
def index():
    articles = Articles.query
    chapters = (
        articles.filter(Articles.chapter != "#")
        .with_entities(Articles.chapter)
        .distinct()
    )
    articles_dict = {
        chapt[0]: articles.filter(Articles.chapter == chapt[0]).all()
        for chapt in chapters
    }
    return render_template("post.html", post_dict=articles_dict)


@post.route("/<post_id>")
def page(post_id):
    articles = Articles.query
    return render_template("page.html", data=articles.get(post_id))
