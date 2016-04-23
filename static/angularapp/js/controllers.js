var app = angular.module('soccerApp.controllers', []);

app.controller('IndexCtrl', function ($scope, Articles) {
	$scope.articles = [];
	$scope.emptyMessage = "Loading content.....";
    $scope.showingMenu = true;

    Articles.get().then(function(articles){
        var dps = ["men_10.jpg", "kerrywashington.jpg", "einstein.jpg", "kingjullian.jpg"];
        var names = ["Justin Kehore", "Olivia Pope", "Einstein Fans", "King Jullian"];

        for (var i = 0; i < articles.length; i++) {
            articles[i].sender = {
                dp : "img/dps/"+dps[i],
                name : names[i]
            }
            $scope.articles.push(articles[i]);
        }
        console.log(articles);
    }, function(error){
        console.log(error);
        $scope.emptyMessage = "We're having some problems loading the content, please check back later.";
    });
});