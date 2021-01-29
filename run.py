from wsb import socketio,app,scraper
thread = socketio.start_background_task(target=lambda: scraper.run(True))   
if __name__ == "__main__":
  socketio.run(app, debug=True) 
   

