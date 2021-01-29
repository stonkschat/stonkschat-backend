import sys
import os

from wsb import db

if __name__ == "__main__":
  if sys.argv[1]:
    if sys.argv[1] == "-r" or "--hardReset":
      os.system("rm -rf wsb/posts.db")
      db.create_all()
      print("Reset complete.")