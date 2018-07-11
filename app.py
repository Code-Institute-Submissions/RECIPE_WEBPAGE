import os
import pymysql
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

""" connect the my sql database """

username = os.getenv('C9_USER')

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user=username,
                             password='',
                             db='recipe_website')

app = Flask(__name__)

""" connent to MONGO DATABASE """

app.config["MONGO_DBNAME"] = "recipes"
app.config["MONGO_URI"] = "mongodb://russ_recipe:recipe1@ds119651.mlab.com:19651/recipes"

mongo = PyMongo(app)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/main")
def main():
    _all_recipes = mongo.db.recipe.find()
    recipes_list = [recipe for recipe in _all_recipes]
    return render_template("main.html", recipes=recipes_list)

@app.route("/login")
def login():
    return render_template("login.html")
    
@app.route("/register")
def register():
    
    return render_template("register.html")
    
    
@app.route("/your_recipes")
def your_recipes():
    
    return render_template("your_recipes.html")
""" CRUD for recipes """

@app.route("/add_recipe")
def add_recipe():
    _cuisine = mongo.db.cuisine.find()
    cuisine_list = [cusines for cusines in _cuisine]
    return render_template("addrecipe.html", cuisine=cuisine_list)
    
@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    recipe = mongo.db.recipe
    recipe.insert_one(request.form.to_dict())
    return redirect( {{ url_for("main") }})

""" CRUD for cuisine """

@app.route("/cuisine")
def cuisine():
    return render_template("cuisine.html", cuisine=mongo.db.cuisine.find())
    
@app.route("/add-cuisine")
def add_cuisine():
    return render_template("add_cuisine.html")
    
@app.route("/insert_cuisine", methods=["POST"])
def insert_cuisine():
    cuisine = mongo.db.cuisine
    cuisine.insert_one(request.form.to_dict())
    return redirect( {{ url_for("cuisine") }})

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get('PORT')),
            debug=True)