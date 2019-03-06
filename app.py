import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
import pymysql
import json
from werkzeug.utils import secure_filename

"""upload path to store photos submitted from recipes"""

UPLOAD_FOLDER = "./static/images"
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.secret_key = os.environ.get('KEY')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


""" connection to my sql database """

connection = pymysql.connect(host=os.environ.get("DB_HOST"),
                             user=os.environ.get("DB_USER"),
                             password=os.environ.get("DB_PASSWORD"),
                             db=os.environ.get("DB_NAME"))
cursor = connection.cursor(pymysql.cursors.DictCursor)


# LOGIN AND REGISTER ROUTES

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["name"]
        user = cursor.execute("SELECT * FROM USERS WHERE name=%s", [username])
        if user != 0:
            flash("Sorry this username is taken, please try again", "red black-text lighten-2")
        else:
            if request.form["password"] == request.form["re-enter"]:
                cursor.execute("INSERT INTO USERS(name, password) VALUES(%s, %s)",
                               (request.form["name"], request.form["password"]))
                connection.commit()
                flash("Welcome to little recipes, username created!!", "blue black-text lighten-2")
                return redirect(url_for("login"))
            else:
                flash("Passwords don't match", "red black-text lighten-2")
    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
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
                flash("Please check username or password", "red black-text lighten-2")
        else:
            flash("Please check username or password", "red black-text lighten-2")
    return render_template("login.html")


# MAIN TEMPLATES

@app.route("/main/")
def main():
    cursor.execute("SELECT * FROM RECIPES ORDER BY date_entered DESC")
    all_recipes = cursor.fetchall()
    cursor.execute("SELECT DISTINCT cuisine FROM RECIPES")
    cuisines = cursor.fetchall()

    ids = []
    rating = []

    for recipe in all_recipes:
        ids.append(recipe['recipe_id'])
    for id in ids:
        cursor.execute("SELECT recipe_id,AVG(rating) FROM REVIEWS WHERE recipe_id = %s", (id))
        rate = cursor.fetchall()
        rating += rate
    return render_template("main.html", all_recipes=all_recipes,
                           cuisines=cuisines,
                           rating=rating)


# CREATE/READ/UPDATE/DELETE FUNCTIONS


@app.route("/your_recipes/", methods=["POST", "GET"])
def your_recipes():
    username = session["name"]
    cursor.execute("SELECT user_id FROM USERS WHERE name =%s", username)
    userId = cursor.fetchone()["user_id"]
    cursor.execute("SELECT * FROM RECIPES WHERE user_id = %s", userId)
    filtered_recipes = cursor.fetchall()

    ratings = []
    for rate in filtered_recipes:
        id = rate["recipe_id"]
        cursor.execute("SELECT * FROM REVIEWS WHERE recipe_id = %s", (id))
        all_ratings = cursor.fetchall()
        ratings.append(all_ratings)
    return render_template("your_recipes.html", your_recipes=filtered_recipes,
                           rating=ratings)


@app.route("/view_recipe/<int:id>")
def view_recipe(id):
    cursor.execute("SELECT * FROM RECIPES WHERE recipe_id = %s", id)
    recipesId = cursor.fetchone()
    cursor.execute("SELECT * FROM INGREDIENTS "
                   "INNER JOIN RECIPES_INGREDIENTS ON ingredient_id = ingredients_id WHERE recipes_id = %s", id)
    recipes_ingredients = cursor.fetchall()
    cursor.execute("SELECT * FROM REVIEWS WHERE recipe_id = %s", (id))
    reviews = cursor.fetchall()
    method = recipesId["method"].split("|")

    return render_template("view_recipe.html", recipe=recipesId,
                           ingredient=recipes_ingredients,
                           methods=method,
                           id=id,
                           reviews=reviews)


@app.route("/add_recipe/", methods=["POST", "GET"])
def add_recipe():
    if request.method == "POST":

        # get id of username

        username = session['name']
        cursor.execute("SELECT user_id FROM USERS WHERE name=%s", username)
        usersId = cursor.fetchone()['user_id']

        #  insert into recipes table

        recipe_name = request.form["recipe_name"]
        cuisine = request.form["cuisine"]
        serves = request.form["serves"]
        temp = request.form["temp"]
        time = request.form["cook_time"]
        prep = request.form["prep_time"]
        method = request.form["methods"]
        ingredient = request.form["ingredients"]

        # photos upload handler

        """check if the post request has the file part"""

        if 'file' not in request.files:
            flash('please upload photo')
            return redirect(request.url)
        file = request.files['file']

        """ if user does not select a file or browser
            submits an empty part without filename """

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        Image = filename

        cursor.execute(
            "INSERT INTO RECIPES(user_id, name, recipe_name, cuisine, serves, temp, time, prep, method, image)"
            " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (usersId, username, recipe_name, cuisine, serves, temp, time, prep, method, Image))

        connection.commit()

        form_ingredients = ingredient.split("|")

        cursor.execute("SELECT recipe_id FROM RECIPES WHERE recipe_id=(SELECT MAX(recipe_id) FROM RECIPES)")
        recipe_id = cursor.fetchone()["recipe_id"]

        # CHECK IF INGREDIENT EXISTS IN DATABASE

        cursor.execute("SELECT ingredient FROM INGREDIENTS")
        database_ingredients = cursor.fetchall()

        check_ingredients = []

        for values in database_ingredients:
            check_ingredients.append(values["ingredient"])

        for ingredient in form_ingredients:

            if ingredient in check_ingredients:

                cursor.execute("SELECT ingredient_id FROM INGREDIENTS WHERE ingredient = %s", ingredient)

                ingredient_database_id = cursor.fetchone()["ingredient_id"]

            else:
                cursor.execute("INSERT INTO INGREDIENTS(ingredient) VALUES(%s)", ingredient)

                connection.commit()

                cursor.execute("SELECT ingredient_id FROM INGREDIENTS WHERE ingredient = %s", ingredient)

                ingredient_database_id = cursor.fetchone()["ingredient_id"]

            cursor.execute("INSERT INTO RECIPES_INGREDIENTS(recipes_id, ingredients_id) VALUES(%s, %s)",
                           (recipe_id, ingredient_database_id))

            connection.commit()

            stats()

        flash("Thank you for adding your recipe", "blue black-text lighten-2")

        return redirect(url_for("your_recipes"))

    return render_template("add_recipe.html")


@app.route("/edit_recipe/<int:id>", methods=["GET", "POST"])
def edit_recipe(id):
    """ get recipe to update and user """

    username = session['name']
    cursor.execute("SELECT user_id FROM USERS WHERE name=%s", username)

    cursor.execute("SELECT * FROM RECIPES WHERE recipe_id = %s", id)
    recipe = cursor.fetchone()

    cursor.execute("SELECT * FROM INGREDIENTS "
                   "INNER JOIN RECIPES_INGREDIENTS ON ingredient_id = ingredients_id WHERE recipes_id = %s", id)

    ingredients = cursor.fetchall()

    method = recipe["method"].split("|")
    1
    if request.method == "POST":

        recipe_name = request.form["recipe_name"]
        cuisine = request.form["cuisine"]
        serves = request.form["serves"]
        temp = request.form["temp"]
        time = request.form["cook_time"]
        prep = request.form["prep_time"]
        method = request.form["methods"]
        image = request.form["image"]
        ingredients = request.form["ingredients"].split("|")

        cursor.execute('UPDATE RECIPES SET recipe_name=%s, '
                       'cuisine=%s, '
                       'serves=%s, '
                       'temp=%s, '
                       'time=%s, '
                       'prep=%s,'
                       ' method=%s, '
                       'image=%s'
                       ' WHERE recipe_id=%s',
                       (recipe_name, cuisine, serves, temp, time, prep, method, image, id))

        cursor.execute("DELETE FROM RECIPES_INGREDIENTS WHERE recipes_id = %s", (id))

        cursor.execute("SELECT ingredient FROM INGREDIENTS")
        database_ingredients = cursor.fetchall()

        check_ingredients = []

        for values in database_ingredients:
            check_ingredients.append(values["ingredient"])

        for ingredient in ingredients:
            if ingredient != "":

                if ingredient in check_ingredients:

                    cursor.execute("SELECT ingredient_id FROM INGREDIENTS WHERE ingredient = %s", (ingredient))

                    ingredient_database_id = cursor.fetchone()["ingredient_id"]

                else:
                    cursor.execute("INSERT INTO INGREDIENTS(ingredient) VALUES(%s)", (ingredient))

                    connection.commit()

                    cursor.execute("SELECT ingredient_id FROM INGREDIENTS WHERE ingredient = %s", (ingredient))

                    ingredient_database_id = cursor.fetchone()["ingredient_id"]

                cursor.execute("INSERT INTO RECIPES_INGREDIENTS(recipes_id, ingredients_id) VALUES(%s, %s)",
                               (id, ingredient_database_id))

                connection.commit()

        flash("Recipe has been updated!", "blue black-text lighten-2")
        return redirect(url_for("your_recipes"))

    return render_template("edit_recipe.html", recipe_details=recipe,
                           ingredients=ingredients,
                           method=method)


@app.route("/delete_recipe/<int:id>/")
def delete_recipe(id):
    cursor.execute("DELETE FROM REVIEWS WHERE recipe_id = %s", id)
    cursor.execute("DELETE FROM RECIPES_INGREDIENTS WHERE recipes_id = %s", id)
    cursor.execute("DELETE FROM RECIPES WHERE recipe_id = %s", id)

    connection.commit()

    flash("Recipe has been deleted!", "green black-text lighten-2")

    return redirect(url_for("your_recipes"))


# RATING RECIPES / QUICK ADD / FILTER

@app.route("/review/<id>", methods=["GET", "POST"])
def review(id):
    username = session["name"]

    cursor.execute("SELECT * FROM RECIPES WHERE recipe_id = %s", (id))
    recipe = cursor.fetchone()

    if request.method == "POST":
        review = request.form["review"]
        rating = request.form["rating"]

        cursor.execute("INSERT INTO REVIEWS(recipe_id, review, rating, reviewer) VALUES(%s,%s,%s,%s)",
                       (id, review, rating, username))

        connection.commit()

        flash("Thank you for your review ", "green black-text lighten-2")
        return redirect(url_for("main"))

    return render_template("review.html", recipe=recipe)


@app.route("/quick_add/<int:id>")
def quick_add(id):
    username = session["name"]

    cursor.execute("SELECT * FROM RECIPES WHERE recipe_id = %s", id)
    quick_add = cursor.fetchall()

    cursor.execute("SELECT user_id FROM USERS WHERE name=%s", username)
    newID = cursor.fetchone()

    cursor.execute("SELECT * FROM INGREDIENTS "
                   "INNER JOIN RECIPES_INGREDIENTS ON ingredient_id = ingredients_id WHERE recipes_id = %s", id)
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

    cursor.execute("INSERT INTO RECIPES(user_id, name, recipe_name, cuisine, serves, temp, time, prep, method, image) "
                   "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (users_id, username, recipe_name, cuisine, serves, temp, cook_time, prep, method, Image))

    connection.commit()

    cursor.execute("SELECT recipe_id FROM RECIPES WHERE user_id = %s ORDER BY recipe_id DESC LIMIT 1",
                   (newID["user_id"]))

    recipe_id = cursor.fetchone()["recipe_id"]

    for ingredient in ingredients:
        cursor.execute("INSERT INTO RECIPES_INGREDIENTS(ingredients_id, recipes_id) VALUES(%s, %s)",
                       (ingredient["ingredient_id"], recipe_id))

        connection.commit()

    return redirect(url_for("your_recipes"))


#  FUNCTION FOR SEARCH RECIPES


@app.route("/filter_recipes/", methods=["POST", "GET"])
def filter_recipes():
    if request.method == "POST":

        recipe = request.form["recipe_name"]
        cuisine = request.form["cuisine"]
        ingredient = request.form["ingredient"]
        serves = int(request.form["serves"])
        rating = int(request.form["rating"])
        prep = int(request.form["prep_time"])

        parameters = []
        statement = ""

        if ingredient != "":

            statement += "SELECT * FROM RECIPES " \
                         "INNER JOIN `RECIPES_INGREDIENTS` on RECIPES.`recipe_id` = `RECIPES_INGREDIENTS`.`recipes_id` " \
                         "INNER JOIN `INGREDIENTS` on `ingredients_id` = `ingredient_id` where `ingredient` like %s "
            parameters.append("%" + ingredient + "%")
        else:
            statement += "SELECT * FROM RECIPES WHERE 1"

        if recipe != "":
            statement += " AND recipe_name like %s"
            parameters.append("%" + recipe + "%")

        if cuisine != "":
            statement += " AND cuisine = %s"
            parameters.append(cuisine)

        if prep > 5:
            statement += " AND prep >= %s"
            parameters.append(prep)

        if serves > 1:
            statement += " AND serves >= %s"
            parameters.append(serves)

        if rating > 1:
            statement += " AND recipe_id IN (SELECT recipe_id FROM REVIEWS WHERE rating = %s)"
            parameters.append(rating)

        recipe = cursor.execute(statement, parameters)
        filtered_recipes = cursor.fetchall()

        if recipe != 0:
            return render_template("filter_recipes.html", all_recipes=filtered_recipes)
        else:
            flash("sorry no recipes found!", "blue black-text lighten-2")
            return redirect(url_for('filter_recipes'))

    return render_template("filter_recipes.html")


@app.route("/stats/")
def stats():
    cursor.execute("SELECT * FROM RECIPES")
    recipes = cursor.fetchall()
    Recipes = []
    for recipe in recipes:
        recipeDict = {
            "recipe_name": recipe['recipe_name'],
            "recipe_time": recipe['time'],
            "recipe_serves": recipe['serves'],
            "recipe_prep": recipe['prep'],
            "recipe_cuisine": recipe['cuisine'],
        }
        Recipes.append(recipeDict)

    with open("static/recipes/recipes.json", "w") as json_data:
        json.dump(Recipes, json_data, indent=4)

    return render_template("stats.html")


@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
