from flask import Flask, request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('test.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS User
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              email TEXT,
              region TEXT,
              maxGames INTEGER,
              breached BOOLEAN DEFAULT FALSE,
              lastBreachEmailDate DATETIME DEFAULT NULL
          )''')
conn.commit()
conn.close

@app.route('/newUser', methods=['POST'])
def new_user():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    name = request.form.get('name')
    email = request.form.get('email')
    region = request.form.get('region')
    maxGames = request.form.get('maxGames')

    c.execute('''INSERT INTO User (name, email, region, maxGames, breached, lastBreachEmailDate) 
                 VALUES (?, ?, ?, ?, FALSE, NULL)''', (name, email, region, maxGames))
    conn.commit()
    conn.close()

    return 'User added successfully'

if __name__ == '__main__':
    app.run()
