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

  /* tab2 */
  $scope.tab2 = {};
  $scope.tab2.myupload = {};
  $scope.tab2.myupload.fresh = function(op, ct){
    $http.get(
      '/homepage/myupload/?op=' + parseInt(op) + '&ct=' + parseInt(ct)
    ).success(
      function(response){
        $scope.tab2.myupload.content = response;
        console.log(response);
      }
    )
  };

  /* tab4 */
  $scope.tab4 = {};
  $scope.tab4.upload = {};
  $scope.tab4.upload.files_list = [];
  $scope.tab4.upload.files_dom = {};

  // add files
  document.getElementById('video-upload').onchange = function(){
    files = this.files;
    console.log(files);
    for (var i = 0; i < files['length']; ++i){
      $scope.tab4.upload.files_list.push(files[i]);
    }
    $scope.$apply();
  };

  // add Icon
  document.getElementById('video-upload-icon').onclick = function(){
    document.getElementById('video-upload').click();
  }

  // remove file
  $scope.tab4.upload.remove_file = function($index){
    $scope.tab4.upload.files_list.splice($index, 1);
    console.log($scope.tab4.upload.files_list);
  };

  $scope.tab4.upload.submit = function(){
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

  /* tab responsive */
  $scope.tab_container = {};
  $scope.tab_container.active = 4;
  $scope.tab_container.tab_total = 5;
  for (var i = 0; i <= 5; ++i)
    $scope.tab_container['tab'+parseInt(i)] = {
      'class': "",
      'http': 0
    };

  $scope.tab_container.change_tab = function(new_tab_id){
    $scope.tab_container["tab"+parseInt($scope.tab_container.active)].class = "";
    $scope.tab_container["tab"+parseInt($scope.tab_container.active)].active = 0;
    $scope.tab_container["tab"+parseInt(new_tab_id)].class = "active";
    $scope.tab_container["tab"+parseInt(new_tab_id)].active = 1;
    $scope.tab_container.active = new_tab_id;
    if (new_tab_id == 2){
      if ($scope.tab_container.tab2.http == 0){
        $scope.tab_container.tab2.http = 1;
        $scope.tab2.myupload.fresh(0, 12);
      }
    }
  };

  $scope.test_model = [];
  $scope.test = function(){
    console.log($scope.tab4.upload.files_list);
    console.log($scope.tab4.upload.files_dom);
    console.log(document.getElementById('video-upload'));
  };



  // async
  main = new Promise(function(){
    $scope.tab_container.change_tab($scope.tab_container.active);
  })
  // genericperinfo
  .then(function(){
    $http.get('/homepage/genericperinfo/').success(
      function(response){
        $scope.username.content = response.username;
        $scope.email.content = response.email;
      }
    );
  });
  // file_handle binding
});
