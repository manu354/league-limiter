# checks all users in the database
# to see if the number of their current games is greater than their set limit 
import datetime
import leagueAPI
import sqlite3
import sendgridAPI
import leagueAPI


def check_breaches():
    # first, get all users from our databse
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    #make sure table exists, todo don't create it!
    # c.execute('''CREATE TABLE IF NOT EXISTS User
    #              (id INTEGER PRIMARY KEY AUTOINCREMENT,
    #               name TEXT,
    #               email TEXT,
    #               region TEXT,
    #               maxGames INTEGER,
    #               breached BOOLEAN DEFAULT FALSE)''')

    res = c.execute('SELECT * FROM User')
    users = [dict(row) for row in res.fetchall()]

    print("Checking for breaches...")
    for user in users:
        print(f"Checking {user['name']}...")
        if leagueAPI.get_number_of_games_today(user['name'], user['region']) > user['maxGames']:
            
            #if last breach email date is not null and is today, don't send email
            if user['lastBreachEmailDate'] is not None:
                last_breach_email_date = datetime.datetime.strptime(user['lastBreachEmailDate'], '%Y-%m-%d %H:%M:%S.%f')
                if last_breach_email_date.date() == datetime.datetime.utcnow().date():
                    print(f"last breach email date is today, not sending email")
                    continue
            
            print(f"{user['name']} has breached their daily game limit.")
            # Update the 'breached' column in the database
            c.execute('UPDATE User SET breached = ? WHERE id = ?', (True, user['id']))

            #set last breach email date to now
            c.execute('UPDATE User SET lastBreachEmailDate = ? WHERE id = ?', (datetime.datetime.utcnow(), user['id']))

            # send email to user
            sendgridAPI.send_breach_email(user)

        else:
            print(f"{user['name']} has not breached their daily game limit.")
            # Update the 'breached' column in the database, 
            c.execute('UPDATE User SET breached = ? WHERE id = ?', (False, user['id']))

        #todo the dont send duplicte email logic needs fixing

    print("Done checking for breaches.")
    conn.commit()
    conn.close()
