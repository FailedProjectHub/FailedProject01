'user strict';

/* Controllers */
var homepage = angular.module('homepage', []).config(
  function($interpolateProvider){
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

homepage.controller('homepage', function homepage($scope, $http){
  /* element */
  $http.get('/homepage/genericperinfo/').success(
    function(response){
      $scope.genericperinfo = response
    }
  );

  /* css */
  $scope.top_container = {};
  $scope.top_container.style = {
    'width': document.body.clientWidth,
    'height': 150
  };
  $scope.avatar = {};
  $scope.avatar.style = {'height': 150, 'width': 150};
  $scope.leftMargin = {};
  $scope.leftMargin.style = {
    'width': 30
  };
  $scope.body = {};
  $scope.body.style = {
  };
  $scope.username = {};
  $scope.username.style = {
    'font-size': '30px',
    'height': 70
  }
  $scope.email = {};
  $scope.email.style = {
    'font-size': '20px',
    'height': 60
  }
});
