from flask import Flask, render_template, request
import sqlite3 as sql
from flask_mail import Mail, Message
import os
app = Flask(__name__)

mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'Yourmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'Yourpassword'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)


@app.route('/')
@app.route("/home")
def home():
   con = sql.connect("mydatabase.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from items")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)


@app.route("/sendemail", methods=['POST'])
def sendemail():
    if request.method == "POST":
        selected = request.form.getlist("checkboxes")
    li = selected
    text = request.form['text']
    con = sql.connect("mydatabase.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    rows = []
    for i in li:
        cur.execute("select * from items where name like ?", ('%'+i+'%',))
        row = cur.fetchone();
        rows.append("name = "+ row["name"]+", price = " + row["price"]+", details = " + row["details"]+" ,category = "+row["category"]+", Brand = "+ row["Brand"])
    print(rows)
    msg = Message('Data from Flask - app', sender = 'yourmail@gmail.com', recipients = [text])
    print(text)
    str1 = ''.join(rows)
    msg.body = str1
    mail.send(msg)
    return redirect(url_for('home'))

@app.route('/result',methods = ['POST', 'GET'])
def result():
   text = request.form['text']
   con = sql.connect("mydatabase.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from items where name like ?",('%'+text+'%',))

   rows = cur.fetchall();
   return render_template("list.html",search = text ,rows = rows)


   
if __name__ == '__main__':
   app.run(debug = True)
