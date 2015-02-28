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
  $scope.tab_container.tab_total = 5;
  $scope.tab_container.tab0 = {'class':"active", 'active':1};
  for (var i = 1; i <= 5; ++i)
    $scope.tab_container['tab'+parseInt(i)] = {'class':"", 'active':0};

  $scope.tab_container.change_tab = function(new_tab_id){
    $scope.tab_container["tab"+parseInt($scope.tab_container.active)].class = "";
    $scope.tab_container["tab"+parseInt($scope.tab_container.active)].active = 0;
    $scope.tab_container["tab"+parseInt(new_tab_id)].class = "active";
    $scope.tab_container["tab"+parseInt(new_tab_id)].active = 1;
    $scope.tab_container.active = new_tab_id;
  }

  /* upload files */
  $scope.tab_container.tab4.upload = {};
  $scope.tab_container.tab4.upload.submit = function(){
    var files = document.getElementById("upload-file").files;
    if (files.length){
      var upload = new Uploader(files[0], function(obj){
        console.log(obj);
        document.getElementById("video-sha256-bar").style.width = obj.checksumprog+"%";
        document.getElementById("video-upload-bar").style.width = obj.uploadprog+"%";
      });

      var lastprog=0, inter=5000;
      setInterval(function(){
        if (upload.checksumprog != 100){
          console.log(parseFloat((upload.checksumprog - lastprog)/100*files[0].size/inter).toFixed(3)+"KB/s");
          lastprog = upload.checksumprog;
        }
        else if (lastprog > upload.checksumprog){
          lastprog = 0;
        }
        else {
          console.log(parseFloat((upload.uploadprog - lastprog)/100 * files[0].size/inter).toFixed(3)+"KB/s");
          lastprog = upload.uploadprog;
        }
      }, inter);
    }
  };


  /* css */
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
  $scope.tab_container.style = {
    'margin-top': 32
  }
  $scope.main_area.style = {
    'height': 700,
    'margin-left': -10,
    'margin-right': -13
  }
  $scope.tab_container.tab4.upload.file = {
    'style': {
      'margin-right':20
    }
  }

});
