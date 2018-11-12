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

// <--------------- Functions for quick searching on main page recipes -------------->

let searchBar = document.getElementById("search");

if(searchBar){
    searchBar.addEventListener("keyup", (e) => {
        
    const searchValue = searchBar.value.toUpperCase(),
          recipeBoxes = document.querySelectorAll(".recipe-display"),
          recipeTitle = document.querySelectorAll(".recipes_title");
    
    console.log(recipeBoxes)
    
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
    
const resetSearch = document.getElementById("search_reset");

function recipeReset(e){
    location.reload();
}

