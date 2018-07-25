import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
import pymysql


app = Flask(__name__)
app.secret_key="some secret"

""" connect the my sql database """

username = os.getenv('C9_USER')

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user=username,
                             password='',
                             db='RECIPES')


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST","GET"])
def register():

    if request.method == "POST":
        username = request.form["name"]
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            user = cursor.execute("SELECT * FROM users WHERE name=%s", [username])
            
            if user != 0:
                flash("Sorry this username is taken", "red black-text lighten-2") 
                cursor.close()

            else:
                if request.form["password"] == request.form["re-enter"]:
                    cursor.execute("INSERT INTO users(name, password) VALUES(%s, %s)", (request.form["name"], request.form["password"]))
                    connection.commit()
                    
                    flash("congratulations you can now login", "green black-text")
                    
                else:
                    flash("passwords not the same")
                    cursor.close()
                    
    return render_template("register.html")
    
@app.route("/login", methods=["POST","GET"])
def login():
    
    if request.method == "POST":
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            username = request.form["name"]
            password = request.form["password"]
            user = cursor.execute("SELECT * FROM users WHERE name=%s", [username])
            
            if user > 0:
                row = cursor.fetchone()
                user_password = row["password"]
                
                if password == user_password:
                    session['name'] = username
                    
                    return render_template("main.html")
                else:
                    flash("passwords not matched", "red black-text lighten-2")
                    cursor.close()
            else:
                flash("Sorry username not found", "red black-text lighten-2")
                cursor.close()
                
    return render_template("login.html")
    
@app.route("/main")
def main():
    return render_template("main.html")
    
@app.route("/your_recipes", methods=["POST", "GET"])
def your_recipes():
    
    return render_template("your_recipes.html")
    
    
""" CRUD for recipes """

@app.route("/add_recipe/", methods=["POST", "GET"])
def add_recipe():
    if request.method == "POST":
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cuisine = "spanish"
            recipe_name = request.form["recipe_name"]
            serves = request.form["serves"]
            temp = request.form["temp"]
            time = request.form["cook_time"]
            prep = request.form["prep_time"]
            ingredients = request.form["ingredients"]
            method = request.form["cook_method"]
            
            cursor.execute("INSERT INTO recipe(recipe_name, cuisine, serves, temp, time, prep, ingredients, method) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (recipe_name, cuisine, serves, temp, time, prep, ingredients, method))
            connection.commit()
            
        flash("Congratulations your recipe was added", "blue black-text lighten-2")
        return redirect(url_for("your_recipes"))
    return render_template("add_recipe.html")



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