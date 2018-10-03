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
            values.push($(item).val());
        });
        $('[name=ingredients]').val(values.join(','));
        
        let method_values = [];
        $('[name=method]').each(function(index, item) {
            method_values.push($(item).val());
        });
        $('[name=methods]').val(method_values.join('-'));
        
    });
});


// <---------- Insert lines for recipe form entries -------->

function addIngredient(e) {

    let list = document.getElementById("list"),
        btn = document.getElementById("ingredients-btn"),
        newElement = document.createElement("input");
    
    newElement.setAttribute("type", "text");
    newElement.setAttribute("name", "ingredient");
    list.insertBefore(newElement, btn);
    
}

function addMethod(e) {

    let list = document.getElementById("method_list"),
         btn = document.getElementById("method-btn"),
        newElement = document.createElement("input");
        
    newElement.setAttribute("type", "text");
    newElement.setAttribute("name", "method");

    list.insertBefore(newElement, btn);
}

// <--------------- Functions for quick searching on main page recipes -------------->

let searchBar = document.getElementById("search");

if(searchBar){
    searchBar.addEventListener("keyup", (e)=> {
    let searchValue = searchBar.value.toUpperCase(),
        recipeBoxes = document.querySelectorAll(".recipe-display"),
        recipeTitle = document.querySelectorAll(".recipes_title");
    
    for(let i = 0; i < recipeBoxes.length; i++){
        
        let title = recipeTitle[i].innerHTML;
   
        if (title.indexOf(searchValue) > -1){
            recipeBoxes[i].style.display = "";
        }else{
            recipeBoxes[i].style.display = "none";
        }
    }
    
});
}


let cuisine = document.getElementById("select_cuisine"),
    recipeBoxes = document.querySelectorAll(".recipe-display"),
    recipeCuisine = document.querySelectorAll(".recipes_cuisine");

function recipeSearch(e){
    let cuisineValue = cuisine.value.toUpperCase();

    for(let i = 0; i < recipeBoxes.length; i++){
        
        let title = recipeCuisine[i].innerHTML.toUpperCase();
       
        if (title.indexOf(cuisineValue) > -1){
            recipeBoxes[i].style.display = "";
        }else{
            recipeBoxes[i].style.display = "none";
        }
    }
}
    
let resetSearch = document.getElementById("search_reset");

function recipeReset(e){
    location.reload();
}

// function for advanced search form

// let filter_cuisine = document.getElementById("f_cuisine").value, 
//     filter_rating = document.getElementById("f_rating"),
//     filter_prep_time = document.getElementById("f_prep_time"),
//     filter_cooking_time = document.getElementById("f_cooking_time"),
//     filter_submit = document.getElementById("recipe_filter");
    
// function recipeFilter(e) {
//     let cuisine = filter_cuisine.value,
//         rating = filter_rating.value,
//         prep_time = filter_prep_time.value,
//         cooking_time = filter_cooking_time.value;
    
        
//     filter_submit.submit();
    
// }