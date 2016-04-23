var app = angular.module('soccerApp', ['ngMaterial', 'ui.router', 'relativeDate', 'angular-nicescroll', 'soccerApp.controllers', 'soccerApp.services', 'scholarnet.directives']);

app.config(function ($stateProvider, $urlRouterProvider, $mdThemingProvider) {

	$mdThemingProvider.theme('default')
		.primaryPalette('blue')
		.accentPalette('pink')

    // Redirect any unresolved url
    $urlRouterProvider.otherwise("/");

    $stateProvider

        .state('index', {
            url: "/",
            templateUrl: "/templates/home.html",
            data: {pageTitle: 'Home', pageSubTitle: ''},
            controller: "IndexCtrl"
        });
});