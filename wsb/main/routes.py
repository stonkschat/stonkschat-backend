from flask import Blueprint, render_template

from wsb.models import Post

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
  posts = Post.query.all()
  return render_template("main/index.html", posts=posts, title="Home")