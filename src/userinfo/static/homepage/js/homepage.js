'user strict';

/* Controllers */
var homepage = angular.module('homepage', []).config(
  function($interpolateProvider){
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

homepage.controller('homepage', function homepage($scope, $http){
  /* element */
  $scope.top_container = {};
  $scope.username = {};
  $scope.avatar = {};
  $scope.leftMargin = {};
  $scope.email = {};
  $scope.userinfo = {};
  $scope.body = {};
  $scope.top_pic = {};
  $http.get('/homepage/genericperinfo/').success(
    function(response){
      console.log(response.username);
      $scope.username.content = response.username;
      $scope.email.content = response.email;
    }
  );

  /* css */
  $scope.top_container.style = {
    'width': "100%",
    'height': 150
  };
  $scope.avatar.style = {
    'height': 80, 
    'width': 80,
    'margin-top': 5
  };
  $scope.leftMargin.style = {
    'width': 30
  };
  $scope.body.style = {
    'width': '100%'
  };
  $scope.username.style = {
    'font-size': '35px',
    'height': 45,
  }
  $scope.email.style = {
    'font-size': '20px',
    'height': 40,
  }
  $scope.userinfo.style = {
  }
  $scope.top_pic.style = {
    'width': '100%'
  }
});
