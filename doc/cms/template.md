angularJS模板约定
========================
    1.变ng(anjularJS)表达式形式为{$ expression $}
        ng默认表达式为{{ expresion }}，与django冲突
        要避免冲突，对每个ng模块作如下配置（每个模块都要如此）：
        var app = angular.module("module_name", []).config(function($interpolateProvider) {
                $interpolateProvider.startSymbol('{$');
                $interpolateProvider.endSymbol('$}');
        });

========================
    2.必须采用模块，以防止污染命名空间
        先用app = angular.module("module_name", [])取得模块对象
        再用app.controller("controller_name", function(){ /* implement goes here.. */ })编写控制器
