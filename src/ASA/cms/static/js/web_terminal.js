var app = angular.module("web_terminal", []).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.controller("f", ["$scope", "$http", function($scope, $http){
	$scope.user = "ASA.tv";
	$scope.host = "psycium.xyz";
	$scope.pwd = "/";
	$scope.coms = [];
	$scope.inp = "";
	
	$scope.submit = function(){
		var errorHandler = function(){
			console.log("error");
			$scope.com_type = "error";
			$scope.coms.push({inp:$scope.inp, oup:{"status":"error","msg":"","com_type":$scope.com_type}});
			$scope.inp = "";
		}
		
		$http.get("/cms/" + encodeURI($scope.inp)).
			success(function(data, status){
				//console.log("success");
				if(status != 200){
					errorHandler();
					return;
				}
				else{
					$scope.com_type = $scope.inp.split(" ",1)[0];
					$scope.oup = data;
					$scope.coms.push({inp:$scope.inp, oup:$scope.oup,com_type:$scope.com_type});
					$scope.inp = "";
				}
			}).
			error(errorHandler);
	}
	
	$scope.detectEnter = function(event){
		if(event.keyCode == 13)
			$scope.submit();
	}
}]);

app.controller("ls",["$scope",function($scope){
	//console.log($scope.com);
	if($scope.com.oup.status == "OK"){
		$scope.com.oup.head = $scope.com.oup.msg.splice(0,1)[0];
	}
}]);
