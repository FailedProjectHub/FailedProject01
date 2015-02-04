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
		$http.get("../cms/" + encodeURI($scope.inp)).
			success(function(data, status, headers, config){
				$scope.oup = status == 200 ? data.msg : "encountered an error!";
				$scope.coms.push({inp:$scope.inp, oup:$scope.oup});
				$scope.inp = "";
			}).
			error(function(data, status, headers, config){
				$scope.oup = [["encontered an error!"]];
				$scope.coms.push({inp:$scope.inp, oup:$scope.oup});
				$scope.inp = "";
			});
	}
	
	$scope.detectEnter = function(event){
		if(event.keyIdentifier == "Enter")
			$scope.submit();
	}
}]);
