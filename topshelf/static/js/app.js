/**
* Created by zhilabug on 3/13/14.
*/
var app = angular.module('app', ['ngRoute', 'ui.bootstrap']);

// The factory creates a shared variable called Data that can be accessed and modified by both controllers.
//Data needs to be passed back and forth between both controllers and two API's.
app.factory("Data", function(){
      return {
    sharedObject: {}
  };
});

//This sets up routes for recipe and pantry views, which are the main pages that users will go to.
app.config(['$routeProvider', function($routeProvider){
    $routeProvider.
        when('/:id/pantry/', {templateUrl: '/static/views/pantry.html', controller: PantryCtrl}).
        when('/:id/recipe/', {templateUrl: '/static/views/recipe.html', controller: RecipeCtrl}).
        otherwise({redirectTo: '/'});
}]);
