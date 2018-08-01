import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
import pymysql
from werkzeug.utils import secure_filename
from sql_connection import connection_import

"""upload path to store photos submitted from recipes"""

UPLOAD_FOLDER = './images'
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

"""login and register pages"""

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
                    
                    flash("username has been registered, you can now login", "green black-text")
                    
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
    
    
"""main website templates"""    
    
@app.route("/main")
def main():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        
        recipes = cursor.execute("SELECT * FROM RECIPES")
        
        all_recipes = cursor.fetchall()
        
        
    return render_template("main.html", all_recipes=all_recipes)
    
    
    
@app.route("/your_recipes", methods=["POST", "GET"])
def your_recipes():
    # stuck getting id from results returned.
    
    username = session["name"]

    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        
        user = cursor.execute("SELECT id FROM USERS WHERE name =%s", username)
        userId = cursor.fetchone()["id"]
        
        recipes = cursor.execute("SELECT * FROM RECIPES WHERE user_id = %s", userId)
        filtered_recipes = cursor.fetchall()
        
    return render_template("your_recipes.html", your_recipes = filtered_recipes )

    
""" CRUD for recipes """

@app.route("/add_recipe/", methods=["POST", "GET"])
def add_recipe():
    
    if request.method == "POST":
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            
            """get id of username"""
            
            username = session['name']
            userId = cursor.execute("SELECT id FROM USERS WHERE name=%s", username)
            usersId = cursor.fetchone()
            
            """post recipe form into database"""
            
            recipe_name = request.form["recipe_name"]
            cuisine = "english"
            serves = request.form["serves"]
            temp = request.form["temp"]
            time = request.form["cook_time"]
            prep = request.form["prep_time"]
            ingredients = request.form["ingredients"]
            method = request.form["cook_method"]
            
            
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
            
            # uplaod file variable images = filename for uploading to database.
            
            cursor.execute("INSERT INTO RECIPES(user_id, recipe_name, cuisine, serves, temp, time, prep, ingredients, method, image) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)", (usersId["id"], recipe_name, cuisine, serves, temp, time, prep, ingredients, method, Image))
            
            connection.commit()
            
        flash("Thank you for adding your recipe", "blue black-text lighten-2")
        return redirect(url_for("your_recipes", filename=filename))
    return render_template("add_recipe.html")


@app.route("/edit_recipe/<int:id>", methods=["GET","POST"])
def edit_recipe(id):
    
    """get recipe to update by id"""
    
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        username = session['name']
        userId = cursor.execute("SELECT id FROM USERS WHERE name=%s", username)
        usersId = cursor.fetchone()
        
        recipeId = cursor.execute("SELECT * FROM RECIPES WHERE id = %s", id)
        recipesId = cursor.fetchone()
        
        if request.method == "POST":
           
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
            
            # uplaod file variable images = filename for uploading to database.
            
            update_list = [(request.form["recipe_name"], 
                            "english", 
                            request.form["serves"], 
                            request.form["temp"], 
                            request.form["cook_time"], 
                            request.form["prep_time"], 
                            request.form["ingredients"], 
                            request.form["cook_method"])]
          
            cursor.execute("UPDATE RECIPES SET recipe_name=%s, cuisine=%s, serves=%s, temp=%s, time=%s, prep=%s, ingredients=%s, method=%s, image=Image WHERE id=%s", (update_list, id))
            
            connection.commit()
        
    return render_template("edit_recipe.html", recipe_details=recipesId)

@app.route("/delete_recipes/<int:id>/")
def delete_recipe(id):

    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        
        delete_recipe = cursor.execute("DELETE FROM RECIPES WHERE id = %s", id)
        connection.commit()
        
    return redirect(url_for("your_recipes"))

@app.route("/cuisine")
def cuisine():
    return render_template("cuisine.html", )
    
@app.route("/add-cuisine")
def add_cuisine():
    return render_template("add_cuisine.html")
    
@app.route("/insert_cuisine", methods=["POST"])
def insert_cuisine():
    return redirect( {{ url_for("cuisine") }})


@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get('PORT')),
            debug=True)