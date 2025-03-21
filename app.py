from flask import Flask, render_template, request, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "random"
con = sqlite3.connect("Database.db")
cur = con.cursor()
cur.execute(""" CREATE TABLE IF NOT EXISTS User(
                Username VARCHAR(20) NOT NULL PRIMARY KEY,
                Password VARCHAR(64) NOT NULL);
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
        hash = hashlib.sha256(request.form['Password'].encode()).hexdigest()
        cur.execute("INSERT INTO User (Username, Password) VALUES (?,?)",
                        (request.form['Username'], hash))
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
        hash = hashlib.sha256(request.form['Password'].encode()).hexdigest()
        cur.execute("SELECT * FROM User WHERE Username=? AND Password=?",
                        (request.form['Username'], hash))
        if len(cur.fetchall()) == 0:
            return "Wrong username and password"
        else:
            session['Username'] = request.form['Username']
            return render_template("welcome.html")

@app.route("/password", methods=["GET", "POST"])
def password():
    if request.method == "GET":
        if 'Username' in session:
            return render_template("password.html")
        else:
            return render_template("index.html")
    else:
        if 'Username' in session:
            con = sqlite3.connect("Database.db")
            cur = con.cursor()
            hash = hashlib.sha256(request.form['NewPassword'].encode()).hexdigest()
            cur.execute("UPDATE User SET Password=? WHERE Username=?",
                            (hash, session['Username']))
            con.commit()
            con.close()
            return "Password changed successfully"
        else:
            return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop('Username', None)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)