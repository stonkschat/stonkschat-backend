from wsb import socketio,app,scraper
from wsb import Config
import argparse
import logging

def parse_args():
    parser = argparse.ArgumentParser(description = "stonks backend")
    parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity")
    parser.add_argument("-p", "--printToConsole", action="store_true",
                    help="increase output verbosity")

    args = parser.parse_args()

    try:
        loglevel = {
            0: logging.ERROR,
            1: logging.WARN,
            2: logging.INFO
        }[args.verbose]
    except KeyError:
        loglevel = logging.DEBUG

    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    c_handler = logging.StreamHandler()
    c_handler.setFormatter(c_format)

    logging.basicConfig(level = logging.WARN, format="%(asctime)s: %(message)s", datefmt="%H:%M:%S")
    logger = logging.getLogger("reddit_scraper")
    logger.setLevel(loglevel)
    logger.addHandler(c_handler)

    if args.printToConsole :
        Config.SOCKETS = False
    else:
        Config.SOCKETS = True
    return args 

thread = socketio.start_background_task(target=lambda: scraper.run(True))   

if __name__ == "__main__":
    parse_args()
    logging.info("starting")
    socketio.run(app, debug=True) 
   

