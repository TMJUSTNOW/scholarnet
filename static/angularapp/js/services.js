angular.module('soccerApp.services', [])

.factory('Articles', ['$http', '$q', function($http, $q) {
    return {
        get: function() {
            var def = $q.defer();
            $http.get("data/articles-list.json")
              .success(function(data) {
                def.resolve(data);
              })
              .error(function() {
                  def.reject("Failed to load articles.");
              });

            return def.promise;
        }
    }
}]);