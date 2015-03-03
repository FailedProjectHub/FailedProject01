'use strict'

/* Controller */

var index = angular.module('index', []).config(
  function($interpolateProvider){
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
  }
);


index.controller('index', function index($scope, $http){
  /* element */
  $scope.collections = [];
  $http.post(
    '/cms/', 
    {
      'command': ['ls', '/public', '--include=folderattrib'],
      'path': '/'
    }
  ).success(
    function(response){
      for (var i in response.msg[0]){
        $scope.collections.push(response.msg[0][i].substr(8));
      }
      console.log($scope.collections);
    }
  ).error(
    function(response){
      console.log(response);
    }
  );

  /* css */
  $scope.style = {};
  $scope.style.collections = {
    'height': 300,
    'margin-bottom': 20
  }
});
