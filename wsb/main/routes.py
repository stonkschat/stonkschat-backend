from flask import Blueprint, render_template

from wsb.models import Thread

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
  threads = Thread.query.all()
  return render_template("main/index.html", threads=threads, title="Home")