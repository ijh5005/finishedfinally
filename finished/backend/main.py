from flask import Flask  # Import Flask
from flask import render_template  # Import render template function
import mysql.connector

app = Flask(__name__)

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'connectiondb'
}

def getCount():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM connection_count')

    results = [current_count for current_count in cursor]

    cursor.close()
    connection.close()

    return results[0][1]

def incrementCount():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    currentCount = int(getCount())
    newCount = currentCount + 1

    cursor.execute(f"UPDATE connection_count SET current_count={newCount} WHERE id=1")
    connection.commit()

    cursor.close()
    connection.close()

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
    app.debug = True
    app.run("0.0.0.0", 5000, debug=True)
