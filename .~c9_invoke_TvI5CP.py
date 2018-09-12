import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
import pymysql
from werkzeug.utils import secure_filename
from sql_connection import connection_import

"""upload path to store photos submitted from recipes"""

UPLOAD_FOLDER = "./static/images"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key="some secret"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

""" connection to my sql database """

# Connect to the database
connection = connection_import

@app.route("/")
@app.route("/index")
def index():
    
    return render_template("index.html")

# <-------------- LOGIN AND REGISTER ROUTES --------------->

@app.route("/register", methods=["POST","GET"])
def register():

    if request.method == "POST":
        username = request.form["name"]
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            user = cursor.execute("SELECT * FROM USERS WHERE name=%s", [username])
            
            if user != 0:
                flash("Sorry this username is taken, please try again", "red black-text lighten-2") 
                cursor.close()

            else:
                if request.form["password"] == request.form["re-enter"]:
                    cursor.execute("INSERT INTO USERS(name, password) VALUES(%s, %s)", (request.form["name"], request.form["password"]))
                    connection.commit()
                    
                    cursor.execute("SELECT user_id FROM USERS WHERE name = %s", (request.form["name"]))
                    id = cursor.fetchone()
    
                    cursor.execute("INSERT INTO USERS_RECIPES(users_id) VALUES(%s)", (id["user_id"]))
                    connection.commit()
                    
                    return redirect(url_for("login"))
                    
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
            user = cursor.execute("SELECT * FROM USERS WHERE name=%s", [username])
            
            if user > 0:
                row = cursor.fetchone()
                user_password = row["password"]
                
                if password == user_password:
                    session['name'] = username
                    
                    return redirect(url_for("main"))
                else:
                    flash("passwords not matched", "red black-text lighten-2")
                    cursor.close()
            else:
                flash("Sorry username not found", "red black-text lighten-2")
                cursor.close()
                
        
    return render_template("login.html")
    
    
# <------------------------ MAIN TEMPLATES ------------------->   
                
@app.route("/main/")
def main():
  
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        
        recipes = cursor.execute("SELECT * FROM RECIPES")
        all_recipes = cursor.fetchall()
        
        cursor.execute("SELECT DISTINCT cuisine FROM RECIPES")
        cuisines = cursor.fetchall()
        
        cursor.execute("SELECT DISTINCT date_entered FROM RECIPES")
        
        
    
    return render_template("main.html", all_recipes=all_recipes, cuisines=cuisines)
    
@app.route("/next/<string:all_recipes>")
def next(all_recipes):
    next(all_recipes)
    return redirect(url_for("main"))
# <--------------------- CRUD for recipes ----------------------->


@app.route("/your_recipes/", methods=["POST", "GET"])
def your_recipes():
    
    # stuck getting id from results returned.
    username = session["name"]

    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        
        cursor.execute("SELECT user_id FROM USERS WHERE name =%s", username)
        userId = cursor.fetchone()["user_id"]

        cursor.execute("SELECT * FROM RECIPES WHERE user_id = %s", userId)
        filtered_recipes = cursor.fetchall()
        
    return render_template("your_recipes.html", your_recipes = filtered_recipes )



@app.route("/view_recipe/<int:id>")
def view_recipe(id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM RECIPES WHERE recipe_id = %s", id)
        recipesId = cursor.fetchone()
        
        cursor.execute("SELECT * FROM INGREDIENTS WHERE recipe_id = %s", id)
        recipes_ingredients = cursor.fetchall()
        
        method = recipesId["method"].split("-")

    return render_template("view_recipe.html", recipe = recipesId, ingredient = recipes_ingredients, methods = method)
    
    
    
@app.route("/add_recipe/", methods=["POST", "GET"])
def add_recipe():
    username = session["name"]
   
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        
        cursor.execute("SELECT DISTINCT CUISINE FROM CUISINE")
        cuisine = cursor.fetchall()

    if request.method == "POST":
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            
            """get id of username"""
            
            username = session['name']
            cursor.execute("SELECT user_id FROM USERS WHERE name=%s", username)
            usersId = cursor.fetchone()
       
            
            """post recipe form into database"""
            
            """insert into recipes table """
            
            recipe_name = request.form["recipe_name"]
            cuisine = request.form["cuisine"]
            serves = request.form["serves"]
            temp = request.form["temp"]
            time = request.form["cook_time"]
            prep = request.form["prep_time"]
            method = request.form["methods"]
            ingredient = request.form["ingredients"]
        
            """photos upload handler"""
             
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('please upload photo')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            Image = filename
            
            cursor.execute("INSERT INTO RECIPES(user_id, name, recipe_name, cuisine, serves, temp, time, prep, method, image) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (usersId["user_id"], username, recipe_name,cuisine, serves, temp, time, prep, method, Image))
    
            connection.commit()

            x = ingredient.split(",")
            
            cursor.execute("SELECT recipe_id FROM RECIPES WHERE recipe_id=(SELECT MAX(recipe_id) FROM RECIPES)")
            
            recipe_id = cursor.fetchone()["recipe_id"]
        
            # <------- CHECK IF INGREDIENT ISNT ALREADY IN DATABASE LIST --------->
            
            cursor.execute("SELECT ingredient FROM INGREDIENTS")
            database_ingredients = cursor.fetchall()
            
            check_ingredients = []
            
            for values in database_ingredients:
                check_ingredients.append(values["ingredient"])

            for i in x:
                if i in check_ingredients:
                    cursor.execute("SELECT ingredient_id FROM INGREDIENTS WHERE ingredient = %s", (i))
                    ingredient_database_id = cursor.fetchone()["ingredient_id"]
                    
                    cursor.execute("INSERT INTO INGREDIENTS(recipe_id) VALUES(%s) WHERE ingredient_id = %s", (recipe_id, ingredient_database_id))
                
                    connection.commit() 
                    
                else:
                    cursor.execute("INSERT INTO INGREDIENTS(ingredient, recipe_id) VALUES(%s, %s)", (i, recipe_id))
                    
                    connection.commit()
                    
            
            connection.commit()
            
        flash("Thank you for adding your recipe", "blue black-text lighten-2")
    
        return redirect(url_for("your_recipes"))
    return render_template("add_recipe.html", cuisines=cuisine)
        

@app.route("/edit_recipe/<int:id>", methods=["GET","POST"])
def edit_recipe(id):
    
    """ get recipe to update and user """
   
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        
        username = session['name']
        cursor.execute("SELECT user_id FROM USERS WHERE name=%s", username)
        usersId = cursor.fetchone()["user_id"]
    
        
        cursor.execute("SELECT * FROM RECIPES WHERE recipe_id = %s", id)
        recipe = cursor.fetchone()
            
        cursor.execute("SELECT * FROM INGREDIENTS WHERE recipe_id = %s", id)
        ingredients = cursor.fetchall()
        
        
        
        method = recipe["method"].split("-")

        if request.method == "POST":
            
            recipe_name = request.form["recipe_name"]
            cuisine = request.form["cuisine"]
            serves = request.form["serves"]
            temp = request.form["temp"]
            time = request.form["cook_time"]
            prep = request.form["prep_time"]
            method = request.form["methods"]
            image = request.form["image"]
            ingredient = request.form["ingredients"].split(",")
             

            cursor.execute('UPDATE RECIPES SET recipe_name=%s, cuisine=%s, serves=%s, temp=%s, time=%s, prep=%s, method=%s, image=%s WHERE recipe_id=%s',(recipe_name, cuisine, serves, temp, time, prep, method, image, id))
            
            cursor.execute("DELETE FROM INGREDIENTS WHERE recipe_id = %s", (id))
            
            for i in ingredient:
                cursor.execute("INSERT INTO INGREDIENTS(ingredient, recipe_id) VALUES(%s, %s)", (i, id))

            connection.commit()
            
            flash("Recipe has been updated!", "blue black-text lighten-2")
            return redirect(url_for("your_recipes"))
        
    return render_template("edit_recipe.html", recipe_details=recipe, ingredients=ingredients, method=method)


@app.route("/delete_recipe/<int:id>/")
def delete_recipe(id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("DELETE FROM RECIPES WHERE recipe_id = %s", id) 
        print(id)
        connection.commit()
        
    return redirect(url_for("your_recipes"))
    
    
# <------------------ RATING RECIPES / QUICK ADD / FILTER ---------------------> 

@app.route("/rate_recipe/<int:id>")
def rate_recipe(id):
  
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM RECIPES WHERE id = %s", id)
        recipe_for_rating = quick_add = cursor.fetchone()
        # rating = request.form["rating"]
        
        # cursor.execute("INSERT INTO RATING(rating, recipe_id, user_id) VALUES(rating = %s, recipe_id = recipe_for_rating['id'], user_id = recipe_for_rating['user_id']", rating)
        
        # cursor.commit()

        
        # print(request.form["showVal"])
        
        
    return redirect(url_for("main"))


@app.route("/quick_add/<int:id>")
def quick_add(id):
    
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        
        username = session["name"]
       
        cursor.execute("SELECT * FROM RECIPES WHERE recipe_id = %s", id)
        quick_add = cursor.fetchall()
        
        cursor.execute("SELECT user_id FROM USERS WHERE name=%s", username)
        newID = cursor.fetchone()
        
        cursor.execute("SELECT * FROM INGREDIENTS WHERE recipe_id = %s", id)
        ingredients = cursor.fetchall()
        
        quick_add[0]['user_id'] = newID["user_id"]
        users_id = quick_add[0]["user_id"]
        recipe_name = quick_add[0]["recipe_name"]
        cuisine = quick_add[0]["cuisine"]
        serves = quick_add[0]["serves"]
        temp = quick_add[0]["temp"]
        cook_time = quick_add[0]["time"]
        prep = quick_add[0]["prep"]
        method = quick_add[0]["method"]
        Image = quick_add[0]["image"]

        cursor.execute("INSERT INTO RECIPES(user_id, name, recipe_name, cuisine, serves, temp, time, prep, method, image) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (users_id, username, recipe_name, cuisine, serves, temp, cook_time, prep, method, Image))

        # for i in ingredients:
        #     cursor.execute("INSERT INTO INGREDIENTS(ingredient, recipe_id) VALUES(%s, %s)", (i, i["recipe_id"])) 

        
        # connection.commit()
        
    return redirect(url_for("your_recipes"))


# @app.route("/filter_recipes")
# def filter_recipes():
#     if request.method == "POST":
#         return redirect(url_for("filter_recipes"))
#     return render_template("filter_recipes.html")

# <------------------ CUISINE SECTION ----------------------->

@app.route("/cuisine")
def cuisine():
    
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT cuisine FROM RECIPES")
        cuisine = cursor.fetchall()
        
    return render_template("cuisine.html", cuisine=cuisine )
    
@app.route("/view_cuisine/<string:cuisine>")
def view_cuisine(cuisine):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM RECIPES WHERE cuisine = %s", cuisine)
        cuisine_view = cursor.fetchall()

    return render_template("view_cuisine.html", view_cuisines = cuisine_view)

@app.route("/add_cuisine")
def add_cuisine():
    
    return render_template("add_cuisine.html")
    



@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get('PORT')),
            debug=True)