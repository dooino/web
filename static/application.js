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
}])
.factory('Routine', ['$resource', function($resource){
    return $resource('/routines');
}]);

angular.module('DooinosAppControllers', ['DooinosAppServices']);

angular.module('DooinosAppControllers')
.controller('ListController', ['$scope', 'Dooinos', 'Routine', function($scope, Dooinos, Routine) {
  $scope.dooinos = Dooinos.query();
  $scope.routines = Routine.query();
}])
.controller('NewRoutineController', ['$scope', '$location', 'Dooinos', 'Routine', function($scope, $location, Dooinos, Routine) {
  $scope.dooinos = Dooinos.query({}, function(){
    $scope.ins = [];
    $scope.outs = [];

    $scope.dooinos.map(function(dooino) {
      dooino["in"].forEach(function(url) { // in is reserved
        $scope.ins.push({
          id: url.action,
          name: dooino.name + " " + url.name
        });
      });
    });

    $scope.dooinos.map(function(dooino) {
      dooino.out.forEach(function(url) {
        $scope.outs.push({
          id: url.action,
          name: dooino.name + " " + url.name
        });
      });
    });
  });

  $scope.createRoutine = function() {
    Routine.save({
      selectedOut: $scope.selectedOut,
      selectedOperation: $scope.selectedOperation,
      selectedValue: $scope.selectedValue,
      selectedIn: $scope.selectedIn,
    });

    $scope.selectedOut = null;
    $scope.selectedOperation = null;
    $scope.selectedValue = null;
    $scope.selectedIn = null;

    $location.path("/");
  };
}]);
