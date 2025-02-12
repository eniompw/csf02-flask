from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    else:
        Username = request.form["Username"]
        Password = request.form["Password"]
        if Password == '123':
            return 'Hello ' + Username
        else:
            return 'Wrong Password'