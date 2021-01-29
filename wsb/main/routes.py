from flask import Blueprint, render_template

from wsb.models import Thread

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
  # threads = Post.query.all()
<<<<<<< HEAD
  return render_template("main/index.html", threads=[], title="Home")
=======
  return render_template("main/index.html", threads=[], title="Home")
>>>>>>> 57100473357003cff4c243941eee04c23e114018
