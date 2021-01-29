from wsb import db

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(), nullable=False)
  content = db.Column(db.String(), nullable=False)