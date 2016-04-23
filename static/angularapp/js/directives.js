var app = angular.module('scholarnet.directives', []);

app.directive('aPost', function(){
  var directive = {
    // scope: {},
    controller : function($scope){
      $scope.openMenu = function($mdOpenMenu, ev) {
        originatorEv = ev;
        $mdOpenMenu(ev);
        // $scope.article = attrs.post;
      };
    },
    restrict: 'E',
    templateUrl: 'templates/apost.html',
    link: link
  };

  return directive;

  function link(scope, element, attrs) {
    // scope.article = attrs.post;
    // console.log(scope.article);
  }
});