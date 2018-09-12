$(document).ready(function() {
    $('.modal').modal();
    $('.sidenav').sidenav();
    $('.slider').slider();
    $('select').formSelect();
    
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


// <---------- Insert line for recipe form entries -------->

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

let searchBar = document.getElementById("search");

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
