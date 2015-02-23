function Session(username, method){
	if(typeof username !== "string")
		throw TypeError();
	
	method = method.toUpperCase();
	
	if(!(method in {'GET':"", 'POST':""}))
		throw Error(method + ' is not a valid HTTP method.');
	
	Session.extend(this,{
		username: username,
		host: location.hostname,
		preurl: '/cms',
		posturl: '/cms/',
		pwd: "/",
		method: method
	});
}

Session.extend = function(des, src){
	for(var i in src)
		des[i] = src[i];
}

Session.debugMode = true;

Session.ajax = function(method, url, data){
	var self = this;
	return new Promise(function(resolve,reject){
		var req = new XMLHttpRequest();
		
		data = JSON.stringify(data);
		
		if(url[0] !='/')
			url = url + '/';
		
		req.onreadystatechange = function(){
			if(req.readyState == 4){
				if(self.debugMode){
					console.log(method + ' ' + url);
					console.log('status: ' + req.status);
					console.log('respond: ' + req.response);
					if(method == 'POST'){
						console.log('data: ' + data);
					}
				}
				
				if(req.status == 200)
					resolve(JSON.parse(req.response));
				else
					reject(req.status);
			}
		}
		
		req.open(method, url, true);
		req.send(data);
	});
};

Session.command = {
	before:{
		cd: function(path){
				path = path.replace(/\/$/, '');
				if(path === '..'){
					if(this.pwd != '/')
						this.pwd = this.pwd.replace(/\w+\/$/, '');
					return false;
				}
				else if(path === '.')
						return false;
				else return true;
		}
	}, onresolve:{
		cd: function(path){
			this.pwd += path + '/';
		}
	}, onreject:{
	}, after:{
	}
}

Session.prototype.exec = function(input){
	var self = this;
	return new Promise(function(resolve, reject){
		input = input.replace(/^ +/, '');
		input = input.replace(/ +$/, '');
		var arr = input.split(/ +/);
		var com = arr[0];
		var argv = arr.slice(1);
		var promise;
		
		if(com in Session.command.before)
			if(!Session.command.before[com].apply(self, argv)){
				resolve();
				return;
			}
		
		if(self.method === 'GET'){
			var url = self.preurl + self.pwd + input;
			promise = Session.ajax(self.method, url);
		}
		else if(self.method === 'POST'){
			var url = self.posturl, data = { command:arr, path: self.pwd.slice(0,-1) || '/' };
			promise = Session.ajax(self.method, url, data);
		}
		
		promise.then(function(res){
			if(res.status === 'OK'){
				if(com in Session.command.onresolve)
					Session.command.onresolve[com].apply(self, argv);
				resolve(res.msg);
			}
			else{
				if(com in Session.command.onreject)
					Session.command.onreject[com].apply(self, argv);
				reject(res.msg);
			}
		});
		
		promise.catch(function(res){
			if(com in Session.command.onreject)
				Session.command.onreject[com].apply(self, argv);
			reject('Unknown error: HTTP status ' + res);
		});
		
		if(com in Session.command.after)
			Session.command.after[com].apply(self, argv);
	});
}

$(function() {
	var session = new Session('ASA.tv', 'POST');
	var jqconsole = $('#console').jqconsole('Log in @' + session.host + ' as ' + session.username + '\n',
											session.username + '@' + session.host + ':' + session.pwd + ' >>> '	);
	
	var stringify = {
		ls: function(o){
			var str = '';
			for(var i = 0; i < o.length; i++){
				for(var j = 0; j < o[i].length; j++)
					str += o[i][j].replace(session.pwd,"") + ' ';
				str += '\n';
			}

			return str;
		},
	}, errorHandler = {
		ls: function(path){
			return path + '\n';
		},
		unknown: function(data){
			return data + '\n';
		}
	};
	
    var prompt = function() {
        jqconsole.Prompt(true, function (input) {
			input = input.replace(/^ +/, '');
			input = input.replace(/ +$/, '');
			var com = input.split(/ +/)[0];
			
			var next = function(text){
				if(text)
					jqconsole.Write(text, 'jqconsole-output');
				jqconsole.prompt_label_main = session.username + '@' + session.host + ':' + (session.pwd.slice(0,-1) || '/') + ' >>> ';
				prompt();
			}
			
			if(!com)
				next('');
			else{
				var promise = session.exec(input);
				
				promise.then(function(data){
					if(!data || !stringify[com])
						next(null);
					else
						next(stringify[com](data));
				});
				
				promise.catch(function(data){
					if(errorHandler[com])
						next(errorHandler[com](data));
					else
						next(errorHandler.unknown(data));
				});
			}
        });
    };
    prompt();
});
