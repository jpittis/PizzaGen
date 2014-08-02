from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import Form
from wtforms import IntegerField
from wtforms.validators import InputRequired
import sqlite3
app = Flask(__name__)

import os
app.config.update(
    SECRET_KEY = os.urandom(24)
)

path = os.path.dirname(__file__)
db_path = os.path.join(path, "..", "toppings.db")

class ToppingForm(Form):
    cheese = IntegerField("Cheese", default = 1)
    meat = IntegerField("Meat", default = 1)
    veggies = IntegerField("Veggies", default = 1)

def getToppingList(topping_type, amount):
    db = sqlite3.connect(db_path)
    c = db.cursor()
    c.execute('''SELECT name FROM toppings
        WHERE type=? ORDER BY RANDOM() LIMIT ?''',
        (topping_type, amount or 0))
    data = c.fetchall()
    toppinglist = []
    for t in data:
        toppinglist.extend(list(t))
    return toppinglist
    

@app.route("/", methods = ["GET", "POST"])
def pick():
    form = ToppingForm()
    if request.method == 'POST':
        toppinglist = []
        toppinglist.extend(getToppingList("cheese", form.cheese.data))
        toppinglist.extend(getToppingList("meat", form.meat.data))
        toppinglist.extend(getToppingList("veggies", form.veggies.data))
        return render_template("pick.html", form = form, toppinglist = toppinglist)
    print form.validate
    return render_template("pick.html", form = form)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    import os
    app.config.update(
        SECRET_KEY = os.urandom(24)
    )
    app.run(host="0.0.0.0", port=8080, debug=True)
