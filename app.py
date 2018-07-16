import os
from flask import Flask, render_template, redirect, request, url_for
import pymysql


app = Flask(__name__)


""" connect the my sql database """

username = os.getenv('C9_USER')

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user=username,
                             password='',
                             db='recipe_website')


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/login", methods=["POST","GET"])
def login():

    return render_template("login.html")

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        if request.form["password"] == request.form["re-enter"]:
            with connection.cursor() as cursor:
                name = request.form["name"] 
                password = request.form["password"]
                cursor.execute("INSERT INTO users(name, password) VALUES(%s, %s)", (name, password))
                connection.commit()
        else:
            print("sorry passwords dont match")
        # return render_template("login.html")
    return render_template("register.html")
    
    
@app.route("/your_recipes")
def your_recipes():
    
    return render_template("your_recipes.html")
""" CRUD for recipes """

@app.route("/add_recipe")
def add_recipe():
    return render_template("addrecipe.html")
    
@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    return redirect( {{ url_for("main") }})

""" CRUD for cuisine """

@app.route("/cuisine")
def cuisine():
    return render_template("cuisine.html", )
    
@app.route("/add-cuisine")
def add_cuisine():
    return render_template("add_cuisine.html")
    
@app.route("/insert_cuisine", methods=["POST"])
def insert_cuisine():
    return redirect( {{ url_for("cuisine") }})

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get('PORT')),
            debug=True)