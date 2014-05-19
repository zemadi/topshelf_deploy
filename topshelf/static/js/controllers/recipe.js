//This is the controller for the recipe page.

function RecipeCtrl($scope, $http, $routeParams, $location, Data) {

    $scope.recipe = undefined;
    var id = $routeParams.id;
//    console.log(id);

//    Counter to limit the number of items displayed. This is incremented dynamically on user-click.
    $scope.feedLimit = 5;

//Loads up the user's pantry list for additional filtering. Still in development.
    $http.get('/api/v1/pantry/?format=json').
        success(function(user_pantry_list){
            console.log(user_pantry_list);
            $scope.pantry_list = user_pantry_list.objects;
        });

//    Loads user's search preferences to pull search results. Their selections are parsed out and formatted as reqired by the Yummly API.
    $scope.loadData = function(){
        queryParams = Data;
        //    Test to make sure the angular service works.
//        console.log(Data);

        //      Extracts ingredients that will be used as search parameters. This isn't DRY. Also used in pantry.js.
        var include1 = "%26allowedIngredient[]=" + queryParams.first.ing_master.ing_test;
        console.log(include1);
        var include2 = "%26allowedIngredient[]=" + queryParams.second.ing_master.ing_test;
        var include3 = "%26allowedIngredient[]=" + queryParams.third.ing_master.ing_test;

//      Continuation from above. Builds query text so that it can be passed to the django view. I'll eventually add more search params here. The functionality is basically there to filter by diet, allergies, etc. It's just not implemented.
        $http.get('/'+id+'/recipe_data/?queryParams='+include1+include2+include3).
            success(function(food) {
//              Testing out what the search parameters actually look like.
                console.log(include1+include2+include3);
                $scope.food = food
            });


    }

    //Loads user data on open.
    $scope.loadData();


//Recipe detail feature. This is also in development. It reqires a second API call for each result displayed, which is logistically difficult.
    $scope.loadDeets = function(item) {
        $http.get('/'+id+'/recipe_detail_data/?recipe_id='+item.id).
            success(function(data) {
                $scope.deets = data;
                console.log($scope.deets);
            });
    }
}



