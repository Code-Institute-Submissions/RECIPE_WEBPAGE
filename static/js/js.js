$(document).ready(function() {
    
    // functions for Initialization
    $('.modal').modal();
    $('.sidenav').sidenav();
    $('.slider').slider();
    $('select').formSelect();
    $('.collapsible').collapsible();
     
    // functions for adding recipe form functionality
    
    $('.recipe-form').on('submit', function(e) {
        let values = [];
        $('[name=ingredient]').each(function(index, item) {
            if (item.value != ""){
                values.push($(item).val());
            }
        });
        $('[name=ingredients]').val(values.join('|'));
        
        let method_values = [];
        $('[name=method]').each(function(index, item) {
            if (item.value != ""){
                method_values.push($(item).val());
            }
        });
        $('[name=methods]').val(method_values.join('|'));
    });
});

// <---------- Insert lines for recipe form entries -------->

function addIngredient(e) {

    const list = document.getElementById("list"),
          btn = document.getElementById("ingredients-btn"),
          newElement = document.createElement("input");
    
    newElement.setAttribute("type", "text");
    newElement.setAttribute("name", "ingredient");
    list.insertBefore(newElement, btn);
    
}

function addMethod(e) {

    const list = document.getElementById("method_list"),
        btn = document.getElementById("method-btn"),
        newElement = document.createElement("input");
        
    newElement.setAttribute("type", "text");
    newElement.setAttribute("name", "method");

    list.insertBefore(newElement, btn);
}

// <-Functions for quick searching on main page recipes ->

let searchBar = document.getElementById("search");

if(searchBar){
    searchBar.addEventListener("keyup", (e) => {
        
    const searchValue = searchBar.value.toUpperCase(),
          recipeBoxes = document.querySelectorAll(".recipe-display"),
          recipeTitle = document.querySelectorAll(".recipes_title");
    
    
    for(let i = 0; i < recipeBoxes.length; i++){
        
        const title = recipeTitle[i].innerHTML.toUpperCase();
   
        if (title.indexOf(searchValue) > -1){
            recipeBoxes[i].style.display = "";
        }else{
            recipeBoxes[i].style.display = "none";
        }
    }
    
});
}


const cuisine = document.getElementById("select_cuisine"),
    recipeBoxes = document.querySelectorAll(".recipe-display"),
    recipeCuisine = document.querySelectorAll(".recipes_cuisine");

function recipeSearch(e){
    const cuisineValue = cuisine.value.toUpperCase();

    for(let i = 0; i < recipeBoxes.length; i++){
        
        const title = recipeCuisine[i].innerHTML.toUpperCase();
        
        if (title.indexOf(cuisineValue) > -1){
            recipeBoxes[i].style.display = "";
        }else{
            recipeBoxes[i].style.display = "none";
        }
    }
}

if(recipeBoxes){
    function starReviews(){
        recipeBoxes.forEach((box)=>{
            let stars = box.querySelectorAll(".inner-rating");
            let starsTotal = 5
            if(stars.length > 0){
                let scores = box.querySelectorAll(".review-score")[0].innerHTML;
                let percentage = scores / starsTotal * 100;
                let roundedPer = `${Math.round(percentage / 10) * 10}`;
                stars[0].style.width = roundedPer + '%'
            }
        })
    }
    function removeTime(){
        dateEntered = document.querySelectorAll(".date");
        [...dateEntered].map(times => {
            time = times.textContent.slice(0,20)
            times.innerHTML = time
        });
    }
    starReviews()
    removeTime()
}

const resetSearch = document.getElementById("search_reset");

function recipeReset(e){
    location.reload();
}


function photoAdd(e){
    const photoBtn = document.querySelectorAll(".file-path"),
          recipeSubmit = document.getElementById("add-photo");
    if(photoBtn.length > 0){
        recipeSubmit.classList.remove("disabled");
    }
}

let ServeChart = document.getElementById("ServingsChart");
    CuisineChart = document.getElementById("CuisinesChart"),
    PrepChart = document.getElementById("PreparationChart"),
    CookChart = document.getElementById("CookingTimeChart");

if(CuisineChart || ServeChart || PrepChart || CookChart){
    function getResults(){
        fetch('/static/recipes/recipes.json')
            .then(function(response){
                return response.json(); 
            })
            .then(function(data){
                
                let = graphCuisine = [],
                      graphServes = [],
                      graphCookingTime = [],
                      graphPrepTime = [],
                      totalRecipes = data.length,
                      color = [];
                
                data.forEach(function(recipe){
                    graphCuisine.push(recipe.recipe_cuisine);
                    graphServes.push(recipe.recipe_serves);
                    graphCookingTime.push(recipe.recipe_time);
                    graphPrepTime.push(recipe.recipe_prep);
                    color.push("#" + Math.floor(Math.random()*16777215).toString(16))
                });
                
                function CountRecipes(array){
                    let numbers = [],
                        appears = [],
                        prev;
                    
                    array.sort();
                    for (let i = 0; i < array.length; i++) {
                        if(array[i] !== prev){
                            numbers.push(array[i]);
                            appears.push(1);
                        }else {
                            appears[appears.length-1]++;
                        }
                        prev = array[i];
                    }   
                    return[numbers, appears];
                }

                let cuisineTotal = CountRecipes(graphCuisine);
                var myCuisineChart = new Chart(CuisineChart, {
                    
                    type: 'bar',
                    data: {
                        labels: cuisineTotal[0],
                        datasets: [{
                            data: cuisineTotal[1],
                            backgroundColor: color,
                            borderColor: color,
                            borderWidth: 1
                        }]
                    },
                    options: {
                        title: {
    					    display: true,
    						text: 'Cuisines',
    						fontSize: 25,
    					},
                        legend: {
                            display: false,
                        },
                        scales: {
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                        display: true,
                                        labelString: 'Number Of Recipes',
                                    },
                                ticks: {
                                    beginAtZero:true,
                                    max: totalRecipes,
                                }
                            }],
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                        display: true,
                                        labelString: 'Amount of Cuisines',
                                    },
                            }],
                        }
                    }
                }); 
                
                let servesTotal = CountRecipes(graphServes);
                
                var myServeChart = new Chart(ServeChart, {
                    type: 'bar',
                    data: {
                        labels: servesTotal[0],
                            datasets: [{
                                data: servesTotal[1],
                                backgroundColor: color,
                                borderColor: color,
                                borderWidth: 1
                            }]
                        },
                    options: {
                        title: {
    						display: true,
    						text: 'Servings',
    						fontSize: 25,
    					},
                        legend: {
                            display: false,
                        },
                        scales: {
                            yAxes: [{
                                scaleLabel: {
                                        display: true,
                                        labelString: 'Number Of Recipes',
                                    },
                                 ticks: {
                                    beginAtZero:true,
                                    max: totalRecipes,
                                }
                            }],
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                        display: true,
                                        labelString: 'Amount of Servings',
                                    },
                            }],
                        }
                    }
                });
            
                let prepTotal = CountRecipes(graphPrepTime);
                
                var myPrepChart = new Chart(PrepChart, {
                    
                    type: 'bar',
                    data: {
                        labels: prepTotal[0],
                        datasets: [{
                            label: 'Total amount of recipes ',
                            data: prepTotal[1],
                            backgroundColor: color,
                            borderColor: color,
                            borderWidth: 1
                        }]
                    },
                    options: {
                         title: {
    						display: true,
    						text: 'Preparation',
    						fontSize: 25,
    					},
                        legend: {
                            display: false,
                        },
                        scales: {
                            yAxes: [{
                                scaleLabel: {
                                        display: true,
                                        labelString: 'Number Of Recipes',
                                    },
                                 ticks: {
                                    beginAtZero:true,
                                    max: totalRecipes,
                                }
                            }],
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                        display: true,
                                        labelString: 'Prep Time for Recipes (mins)',
                                    },
                            }],
                        }
                    }
                });
                
                let CookingTotal = CountRecipes(graphCookingTime);
                
                var myCookChart = new Chart(CookChart, {
                    
                    type: 'bar',
                    data: {
                        labels: CookingTotal[0],
                        datasets: [{
                            label: 'Total amount of recipes ',
                            data: CookingTotal[1],
                            backgroundColor: color,
                            borderColor: color,
                            borderWidth: 1
                        }]
                    },
                    options: {
                         title: {
    						display: true,
    						text: 'Cooking Time',
    						fontSize: 25,
    					},
                        legend: {
                            display: false,
                        },
                        scales: {
                            yAxes: [{
                                scaleLabel: {
                                        display: true,
                                        labelString: 'Number Of Recipes',
                                    },
                                 ticks: {
                                    beginAtZero:true,
                                    max: totalRecipes,
                                }
                            }],
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                        display: true,
                                        labelString: 'Cooking Time for Recipes (mins)',
                                },
                            }],
                        }
                    }
                });
            });
    }
    getResults();
}
