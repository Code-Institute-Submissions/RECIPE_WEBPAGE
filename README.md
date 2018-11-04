## Data Centric Milestone Project

Little Recipes 


[View Little Recipes Webpage]( https://recipe-page-milestone-project.herokuapp.com/)

Little Recipes website was created for storing all your favourite recipes or to help you find some inspiration on trying something new that others have created.
Adding recipes to your own login domain couldn't be easier with a simple form to fill in that lets you name your recipe and a type of cuisine. Simple to add ingredients
and methods for your recipe and showcase the final piece with a photo. On preview of a recipe there is an easy tick off box for each ingredient you prepare and the method you complete to keep track on what stage your on.

 
## Website Functionality

Little recipes was designed for storing your favourite recipes and sharing them with others. Once a recipe is chosen your are shown all the ingredients in a list along with step by step methods. 

How does Little Recipes work : 

 1. Register a new user or login using your existing user.

 2. Once logged in you are brought to the main webpage where all the recipes that have been created by users are displayed. Each recipe card shown has a small picture shown and 2 buttons beneath. A view button and an add button:

* Click View - will show the recipe only, displaying cooking times, temp, prep time, how many servings , ingredients and methods. Ingredients and methods both have a small tick box next to them to help you keep track of ingredients you have added already or which stage of the methods your currently on.

* Click Add - This will copy the recipe and save it in your own recipes list so you always have it or if you think something needs to be changed to your liking then you can also edit it.
   
 3. All your recipes are kept together by clicking on the your recipes link in the navbar. A list is displayed of the recipes you currently have or you can simply add a new one by clicking on the add recipe button. Adding a new recipe is simply just filling out a form and adding a photo of the final dish for others to view and enjoy.

 4.  Recipes can be reviewed and rated from 1-5. Once rated a small score will be displayed in the corner of your recipe on the main display page for others to see. All reviews are listed at the bottom on a recipe once clicked on the view button.

 5. Once you have finished with a recipe you can delete this by simply clicking on a delete button on your recipe listing page.

 6. Searching for a recipe can be done 2 ways. There is a quick search option on the main recipe display page just underneath the navbar which can search for either a recipe name or cuisine. A more advanced search is also available by clicking the advanced search button where you can search by recipe name, cuisine, rating, servings and preparation time.


## Technologies Used


- [JQuery / Javascript](https://jquery.com)
    - The project uses **JQuery / Javascript** for initialization on materialise elements functionality to make the users have more of an experience using the website. 

- [Python](https://www.python.org/)
    -  **Python**  was the chosen language used to write Little Recipes webpage. Python is a powerful programming language with many builtin functions and extensions. 

- [Flask](http://flask.pocoo.org/)
    - The project uses **Flask** as its a micro framework for python. Flask handles page url routing, Providing templates so HTML code layouts can be passed throughout multiple pages without the need to keep repeating code. Flask has a Debug system which can notify me of any problems that I come across while creating the webpage.

- [Cloud9](https://c9.io/login)
    - **Cloud9** was the chosen IDE (integrated development environment) which is an online program based program. Can be easily accessed from any machine with a login and password.

- [Materialise](https://materializecss.com/)
    - The project uses **Materialise**, a modern responsive front end framework. Materialise is similar to bootstrap making the webpage responsive from being in a mobile view to a large screen or tablet.

- [Sequel Pro](https://www.sequelpro.com/)
    -  **Sequel Pro** is an Apple program which was used to help me maintain my sql database.  The table structure for my database was designed and maintained through Sequel Pro using Primary keys and Foreign keys to help me organise my data being passed through by the webpage.

- [Heroku](https://id.heroku.com/login)
    -  **Heroku** is used for my webpage deployment. My code is committed to Heroku and add a requirements text file and procfile so Heroku knows which software has to be installed and what program my code is running.

## Testing Little Recipes

1. Google Chrome - HTML / Javascript / Jquery / CSS where all tested through the google chrome developer tool. Error message would appear in the console if anything was detected. Errors where displayed with a file location and which line the fault was on. Google chrome developer tools has a responsive section in which my webpage could be tested on many different screen sizes to make sure everything was working correctly for any users screen. 

2. Flask  - Jinja has a built in debug tool. Any Python code that isn't formatted correctly or a response that is being processed to the backend an error message is displayed and the webpage is stopped at the current point the code is broken.

3. Sequel Pro - Any data being based to my database could be easily read. Any incorrect data could be deleted or edited or if any tables or incorrect queries they could be tested in the program without having to use the webpage.

4. Webpage scenario testing was carried out on the login page, register page, recipe adding and search fields making sure the user was alerted if an input had been left blank or incorrectly filled in.


## Deployment

My webpage is deployed through Heroku. I created a Heroku app to which I created a Github repository thorough the command line. i added a requirements text file and a Procfile so Heroku knows what to install and what program my code is running. Once created I added all my code to Heroku and committed my work ready to be pushed to the Heroku branch. 