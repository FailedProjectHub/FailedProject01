'user strict';

/* Controllers */
var homepage = angular.module('homepage', []).config(
  function($interpolateProvider){
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
  }
);

homepage.controller('homepage', function homepage($scope, $http){
  /* element */
  $scope.username = {};
  $scope.email = {};
  $scope.top_container = {};
  $scope.main_area = {};
  $http.get('/homepage/genericperinfo/').success(
    function(response){
      $scope.username.content = response.username;
      $scope.email.content = response.email;
    }
  );

  /* ajax */
  $scope.ajax = {};
  $scope.ajax.myupload = {};
  $scope.ajax.myupload.fresh = function(op, ct){
    $http.get(
      '/homepage/myupload/?op=' + parseInt(op) + '&ct=' + parseInt(ct)
    ).success(
      function(response){
        $scope.ajax.myupload.content = response;
        console.log(response);
      }
    )
  };

  /* tab responsive */
  $scope.tab_container = {};
  $scope.tab_container.active = 4;
  $scope.tab_container.tab_total = 5;
  for (var i = 0; i <= 5; ++i)
    $scope.tab_container['tab'+parseInt(i)] = {'class':""};

  $scope.tab_container.change_tab = function(new_tab_id){
    $scope.tab_container["tab"+parseInt($scope.tab_container.active)].class = "";
    $scope.tab_container["tab"+parseInt($scope.tab_container.active)].active = 0;
    $scope.tab_container["tab"+parseInt(new_tab_id)].class = "active";
    $scope.tab_container["tab"+parseInt(new_tab_id)].active = 1;
    $scope.tab_container.active = new_tab_id;
    if (new_tab_id == 2){
      $scope.ajax.myupload.fresh(0, 12);
    }
  }

  /* upload files */
  $scope.tab_container.tab4.upload = {};
  $scope.tab_container.tab4.upload.submit = function(){
    var files = document.getElementById("upload-file").files;
    if (files.length){
      if (files[0].name.indexOf(' ') >= 0){
        alert("文件名不能带空格");
        return false;
      }
      var upload = new Uploader(files[0], 
        // status
        function(obj){
          console.log(obj);
          document.getElementById("video-sha256-bar").style.width = obj.checksumprog+"%";
          document.getElementById("video-upload-bar").style.width = obj.uploadprog+"%";
        },
        // callback
        function(response){
          submitCover(response.rec);
        }
      );

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


  main = new Promise(function(){
    $scope.tab_container.change_tab($scope.tab_container.active);
  });

  /* css */
  $scope.tab_container.tab4.upload.video_cover_div = {
    'style': {
      'height': 550,
      'margin-top': 20
    }
  }
  $scope.tab_container.tab4.upload.video_cover_nav = {
    'style': {
      'margin-top': 20,
      'height': 530
    }
  };
  $scope.tab_container.tab4.upload.video_cover_file = {
    'style': {
      'margin-top': 20
    }
  };
  $scope.tab_container.tab4.upload.video_cover_preview = {
    'style': {
      "height": 400,
      "width": 400
    }
  };
  $scope.tab_container.tab4.upload.button = {
    'style': {
      'margin-top': 20,
      'margin-bottom': 20,
      'height': 105,
      'width': 260
    }
  };
  $scope.tab_container.tab4.upload.progress = {
    'style': {
      'margin-top': 30,
      'margin-left': 5,
      'margin-right': 5
    }
  };
  $scope.tab_container.tab4.upload.progress_cover = {
    'style': {
      'margin-top': 20
    }
  };
});
