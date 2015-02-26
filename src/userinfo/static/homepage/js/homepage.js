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
  $scope.tab_container = {};
  $scope.main_area = {};
  $http.get('/homepage/genericperinfo/').success(
    function(response){
      $scope.username.content = response.username;
      $scope.email.content = response.email;
    }
  );

  /* tab responsive */


  $scope.tab_container.active = 0;
  $scope.tab_container.old_active = 0;
  $scope.tab_container.tab0 = {'class':"active"};
  $scope.tab_container.tab1 = {'class':""};
  $scope.tab_container.tab2 = {'class':""};
  $scope.tab_container.tab3 = {'class':""};

  $scope.tab_container.change_tab = function(new_tab_id){
    $scope.tab_container["tab"+parseInt($scope.tab_container.active)].class = "";
    $scope.tab_container["tab"+parseInt(new_tab_id)].class = "active";
    $scope.tab_container.active = new_tab_id;
  }

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
  $scope.tab_container.style = {
    'margin-top': 32
  }
  $scope.main_area.style = {
    'height': 700,
    'margin-left': -5,
    'margin-right': -15
  }

});
