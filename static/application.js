var app = angular.module('DooinosApp', [
  'ngRoute',
  'DooinosAppServices',
  'DooinosAppControllers',
]);

app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
  $locationProvider.html5Mode(true);
  $routeProvider
    .when('/', {
      controller:'ListController',
      templateUrl:'/templates/list.html',
    })
    .when('/new', {
      controller:'NewRoutineController',
      templateUrl:'/templates/new.html',
    })
    .otherwise({
      redirectTo:'/'
    });
}]);

angular.module('DooinosAppServices', ['ngResource']);

angular.module('DooinosAppServices')
.factory('Dooinos', ['$resource', function($resource) {
  return $resource('/dooinos', {}, {
    query: {
      method: 'GET',
      isArray: true,
    }
  });
}]);

angular.module('DooinosAppControllers', ['DooinosAppServices']);

angular.module('DooinosAppControllers')
.controller('ListController', ['$scope', 'Dooinos', function($scope, Dooinos) {
  $scope.dooinos = Dooinos.query();
}])
.controller('NewRoutineController', ['$scope', 'Dooinos', function($scope, Dooinos) {
  $scope.dooinos = Dooinos.query({}, function(){
    $scope.ins = $scope.dooinos.map(function(dooino) {
      return {
        id: dooino.name,
        name: dooino.name + " " + dooino["in"][0].name // in is reserved
      };
    });

    console.log($scope.ins);

    $scope.outs = $scope.dooinos.map(function(dooino) {
      return {
        id: dooino.name,
        name: dooino.name + " " + dooino.out[0].name
      };
    });
  });

  $scope.loadDooinos = function() {
    $scope.targetDooinos = function() {
    };
  };
}]);
