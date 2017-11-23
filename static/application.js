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
.controller('ListController', ['$scope', '$http', 'Dooinos', 'Routine', function($scope, $http, Dooinos, Routine) {
  $scope.dooinos = Dooinos.query();
  $scope.routines = Routine.query();

  var operations = ["equals", "greater", "smaller"];

  $scope.mapOperation = function(index){
    return operations[index];
  };

  $scope.handleClick = function(action){
    $http.get(action);
  };
}])
.controller('NewRoutineController', ['$scope', '$location', 'Dooinos', 'Routine', function($scope, $location, Dooinos, Routine) {
  $scope.dooinos = Dooinos.query({}, function(){
    $scope.ins = [];
    $scope.outs = [];

    $scope.dooinos.map(function(dooino) {
      dooino["in"].forEach(function(url) { // in is reserved
        $scope.ins.push({
          id: url.action,
          dooino: dooino.name,
          name: dooino.name + " " + url.name
        });
      });
    });

    $scope.dooinos.map(function(dooino) {
      dooino.out.forEach(function(url) {
        $scope.outs.push({
          id: url.action,
          dooino: dooino.name,
          name: dooino.name + " " + url.name
        });
      });
    });
  });

  $scope.handleOut = function(){
    $scope.selectedOutDooino = $scope.outs.find(function(out){
      return out.id == $scope.selectedOut;
    });
  };

  $scope.handleIn = function(){
    $scope.selectedInDooino = $scope.ins.find(function(_in){
      return _in.id == $scope.selectedIn;
    });
  };

  $scope.createRoutine = function() {

    Routine.save({
      selectedOut: $scope.selectedOut,
      selectedOperation: $scope.selectedOperation,
      selectedValue: $scope.selectedValue,
      selectedIn: $scope.selectedIn,
      selectedOutDooino: $scope.selectedOutDooino.dooino,
      selectedInDooino: $scope.selectedInDooino.dooino,
    });

    $location.path("/");
  };
}]);
