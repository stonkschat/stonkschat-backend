from wsb import db

class Thread(db.Model):
  id = db.Column(db.Integer, primary_key=True)

  thread_id = db.Column(db.String(), nullable=False)
  title = db.Column(db.String(), nullable=False)
  author = db.Column(db.String(), nullable=False)
  content = db.Column(db.String())
  image_url = db.Column(db.String())
  video_url = db.Column(db.String())