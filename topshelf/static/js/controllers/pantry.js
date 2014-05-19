//Main controller for pantry page. Pulls data, posts results, queries and edits the API, among other things.

function PantryCtrl($scope, $http, $routeParams, $location, Data) {
//    Sets scope to the service variable called Data, which shares this variable between the two controllers.
    $scope.queryParams = Data;

//  Gets user id from url, to use in other functions.
    var id = $routeParams.id;
    $scope.id = id;
    $scope.pantry = undefined;

//    Below: Gets the master list of ingredients, which the user can add to their pantry.
// This is for data consistency, to avoid differences like "lemons" and "fresh picked lemons."
    $http.get('/api/v1/all_ingredients/?format=json&limit=0').
        success(function(food){
            list_items = []
//     This populates the autocomplete in pantry.html.
            $scope.list_items = food.objects;
        });


//   Gets the user's pantry. (List of ingredients that they have at home). This runs every time there is a change in the browser.
    $scope.loadData = function(){
        $http.get('/api/v1/pantry/?format=json').
            success(function(user_pantry_list){
                $scope.pantry_data = user_pantry_list.objects;
            });
    }
    //Loads user data on open.
    $scope.loadData();


//    Takes the ingredients a user selects and adds it to their personal inventory.
//    A user's inventory is a subset of the master list of ingredients.
    $scope.submitForm = function() {
        $http.post('/api/v1/pantry/?format=json', $scope.pantry).
            success(function(response){
                $scope.loadData();
            })
    }

//Deletes an item from a user's inventory, on click.
    $scope.deleteItem = function(item) {
        console.log(item);
        $http.delete(item.resource_uri + '?format=json').
            success(function(){
                console.log("Item deleted!")
                $scope.loadData();
            });
    }


//  Sends the user's preferences to an API, which are called in the recipe search.
    $scope.recipeSearchForm = function(queryParams, id) {

//      This sets the data for the service, which is accessed by the other controller.
        Data = queryParams;

//      Extracts ingredients that will be used as search parameters.
//      Builds query text so that it can be passed to the django view. I'll eventually add more search params here like allergies, etc.
//      This isn't DRY. I'll work on it!
        var include1 = "%26allowedIngredient[]=" + queryParams.first.ing_master.ing_test;
        var include2 = "%26allowedIngredient[]=" + queryParams.second.ing_master.ing_test;
        var include3 = "%26allowedIngredient[]=" + queryParams.third.ing_master.ing_test;

//        Actually does the get request to the Yummly api, which goes through a django page.
        $http.get('/'+id+'/recipe_data/?queryParams='+include1+include2+include3).
            success(function(params) {
//              They are formatted in the same way as required by the yummly api.
                console.log(include1+include2+include3);
//                console.log(id);
            });
    }


}
