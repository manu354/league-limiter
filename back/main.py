from datetime import datetime, timezone, timedelta
import leagueAPI
from flask import Flask, send_from_directory
from newUser import *
import threading
import schedule
import time
from checkBreaches import check_breaches

app = Flask(__name__)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


@app.route('/')
def hello():
    return send_from_directory('../front', 'index.html')

@app.route('/newUser', methods=['POST'])
def new_user_route():
    return new_user()

if __name__ == '__main__':
    check_breaches();
    schedule.every(1).minutes.do(check_breaches)

    t = threading.Thread(target=run_schedule)
    t.start()

    app.run()

