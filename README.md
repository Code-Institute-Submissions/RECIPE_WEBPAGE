# Milestone project - Recipe Webpage


### 1. Design / Purpose

Recipe webpage was designed using Materialize. A modern responsive front-end framework.
Materialize is an easy and quick framework to use, similar to bootstrap. 
The man purpose of this webpage is to be able to store all your favourite recipes online. No need to write anything down, just fill out the form and submit and the webpage takes care of the rest.
You are able to share your recipes with others. 
Quickly add someones recipe that you like the look of to your own list.
Easily manage recipes while cooking or preparing by simply clicking the boxes once complete.

### 2. Software used
 
**1.** *Cloud 9*  
Cloud 9 is IDE for writing, running, and debugging code.

**2** *MySQL*
MySQL was used for storing all data from users and password to recipes and ingredients.


### 3. Behind the scenes

**1.** User login - Every user has to have a login and password, so they are unique and stored in database.
**2.** Recipes - Recipes are split into 2 different tables. 
        One table is recipes (recipe name, methods, date created, user id that created the recipe)
        One table is ingredients ( ingredient, the ingredient id to which recipe it belongs to)
**3.** Rating table -  Rating table is for reviews on a recipe and they score 1-5 on what they thought about the recipe selected.

**4.** *Heroku for deployment*
Heroku was used for deployment. Uploaded my code from cloud9, installed requirements.txt and Procfile so heroku could read the file was python and the requirements needed.

**5.** *Python3 / HTML / CSS / Javascript / Jquery*
Python3 - Version 3.6.5
HTML - HTML templates where used throughout and injected pieces of html into blocks to be displayed on the main template(base.html).
CSS - Used CSS for all my styling of the webpage.
Javascript / Jquery - Jquery used for Initialization on functions used in Materialize such as forms and selectors. Javascript used for adding recipes form.

**4.** *Flask*
Flask is a micro framework used for my webpage. 
From flask I imported the following - Flask, render_template, request, redirect, flash and url_for.
These help with url routing and templates being rendered once redirected by the webpage. Flash is used to display messages and request handles GET and POST requests from forms within my webpage.

### 4. Testing
Chrome developer tools was used for testing, if there was anything wrong with my html, css or javascript files I would be alerted quickly. 
Another powerful test tool is flasks jinja error page that appeared when errors where detected, quickly by either stopping my webpage from loading in the browser or not loading a render_template request.

### 5. View Recipe Webpage 

**View Recipe page below by clicking link**
[Play game!!]
(https://git.heroku.com/recipe-page-milestone-project.git)




    
