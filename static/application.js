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

  $scope.dooinoName = function(id){
    return $scope.dooinos.find(function(dooino){
      return dooino.id == id;
    }).name;
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
          value: url.action,
          id: dooino.id,
          name: dooino.name + " " + url.name,
          action: url.name
        });
      });
    });

    $scope.dooinos.map(function(dooino) {
      dooino.out.forEach(function(url) {
        $scope.outs.push({
          value: url.action,
          id: dooino.id,
          name: dooino.name + " " + url.name,
          action: url.name
        });
      });
    });
  });

  $scope.handleOut = function(){
    $scope.selectedOutDooino = $scope.outs.find(function(out){
      return out.value == $scope.selectedOut;
    });
  };

  $scope.handleIn = function(){
    $scope.selectedInDooino = $scope.ins.find(function(_in){
      return _in.value == $scope.selectedIn;
    });
  };

  $scope.createRoutine = function() {
    var data = {
      source: {
        id: $scope.selectedOutDooino.id,
        action: $scope.selectedOutDooino.action
      },
      target: {
        id: $scope.selectedInDooino.id,
        action: $scope.selectedInDooino.action
      },
      condition: {
        value: $scope.selectedValue,
        operation: $scope.selectedOperation
      }
    };

    Routine.save(data);

    $location.path("/");
  };
}]);
