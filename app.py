from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
con = sqlite3.connect("Database.db")
cur = con.cursor()
cur.execute(""" CREATE TABLE IF NOT EXISTS User(
                Username VARCHAR(20) NOT NULL PRIMARY KEY,
                Password VARCHAR(20) NOT NULL);
            """)
con.commit()
con.close()

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        con = sqlite3.connect("Database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO User (Username, Password) VALUES (?,?)",
                        (request.form['Username'],request.form['Password']))
        con.commit()
        con.close()
    return "Signup Successful"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    else:
        con = sqlite3.connect('Database.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM User WHERE Username=? AND Password=?",
                        (request.form['Username'],request.form['Password']))
        if len(cur.fetchall()) == 0:
            return "Wrong username and password"
        else:
            return "Welcome " + request.form['Username']

if __name__ == "__main__":
    app.run(debug=True)