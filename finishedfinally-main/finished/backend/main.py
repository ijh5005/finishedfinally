from flask import Flask  # Import Flask
from flask import render_template  # Import render template function
import mysql.connector

# setting up the app to receieve api requests
app = Flask(__name__)

# credentials for database
config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'connectiondb'
}

def getCount():
    # connect to the mysql database
    connection = mysql.connector.connect(**config)

    # the cursor helps to execute commands on the database
    # ex: getting stuff out of the database, or deleting thing
    cursor = connection.cursor()

    # gets everything from the table
    cursor.execute('SELECT * FROM connection_count')

    # this stores all table databse in array
    results = [current_count for current_count in cursor]

    # closes connection to avoid memory leaks
    cursor.close()
    connection.close()

    # this returns the current_count
    # (id, current_count) => results[0]
    # current_count => (id, current_count)[1]
    return results[0][1]

def incrementCount():

    # connect to the mysql database
    connection = mysql.connector.connect(**config)

    # the cursor helps to execute commands on the database
    # ex: getting stuff out of the database, or deleting thing
    cursor = connection.cursor()

    # get the current count
    currentCount = int(getCount())
    # increment the count to get new count
    newCount = currentCount + 1

    # update the database with the new count
    cursor.execute(f"UPDATE connection_count SET current_count={newCount} WHERE id=1")
    # save the changed in the database
    connection.commit()

    # closes connection to avoid memory leaks
    cursor.close()
    connection.close()

    # we are going to return the new count in the database
    return int(getCount())

@app.route('/')
def count():
    theCount = getCount()
    return render_template("index.html", webCount=theCount)

@app.route('/backend')
def count2():
    theCount = incrementCount()
    return {"count": theCount}

if __name__ == '__main__':
    # this runs the API
    app.run("0.0.0.0", 5000, debug=True)
