from flask import FLask, render_template, request, direct, url_for, flash
import MySQLdb

app = Flask(__name__)

conn = MySQLdb.connect(host="localhost",user="root",password="root",db="email_validation")

@app.route("/")
def index():
    return render_template("index.html", title="signUp")

@app.route("/signUp", methods="[POST"])
def signUp():
    first_name = str(request.form["first_name"])
    last_name = str(request.form["last_name"])
    email = str(request.form["email"])
    password = str(request.form["password"])
    password_confirm = str(request.form["password_confirm"])

    cursor = conn.cursor()

    cursor.execute("INSERT INTO registration (first_name, last_name, email, password, password_confirm) VALUES (%s, %s, %s, %s, %s)", (first_name, last_name, email, password, password_confirm))
    conn.commit()
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True)