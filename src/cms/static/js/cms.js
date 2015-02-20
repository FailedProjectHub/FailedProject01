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

Session.parseConfig = function(config){
		var str = "";
		for(var i in config)
			if(config[i])
				str += '-' + i + ' ';
		return str;
}

Session.formatInput = function(str){
	while(str && str[0] === '/')
		str = str.slice(1);
	while(str && str[str.length-1] === '/')
		str.length --;
	return str;
}

Session.spliceVoid = function(arr){
	var i = 0;
	while(i < arr.length){
		if(!arr[i])
			arr = arr.splice(i,1);
		else
			i++;
	}
	return arr;
}

Session.prototype = {
	constructor: Session,
	cd: function(folder){
		
		var self = this;
		return new Promise(function(resolve, reject){
			folder = Session.formatInput(folder);
			if(typeof folder !== "string"){
				reject('invalid input');
				return;
			}
			
			if(folder == ".."){
				if(self.pwd != '/'){
					//note that pwd ends with a '/', thus we need to invoke slice twice
					self.pwd = self.pwd.slice(0, self.pwd.lastIndexOf('/'));
					self.pwd = self.pwd.slice(0, self.pwd.lastIndexOf('/') + 1);
				}
				resolve();
				return;
			}

			if(folder == '.'){
				resolve();
				return;
			}	
			
			var promise;
			
			if(self.method === 'GET'){
				var url = self.preurl + self.pwd + 'cd ' + folder;
				promise = Session.ajax(self.method, encodeURI(url));
			}
			else if(self.method === 'POST'){
				var url = self.preurl, data = { command: Session.spliceVoid(['cd', folder]), path: self.pwd.slice(1,-1) };
				promise = Session.ajax(self.method, url, JSON.stringify(data));
			}
			
			promise.then(function(res){
				if(res.status == "OK"){
					self.pwd += folder + '/';
					resolve();
				}
				else
					reject(Error(data));
			});
			
			promise.catch(function(code){
				reject(Error("Unknown error: HTTP status " + code));
			});
		});
	},
	/*
		mkdir
		set config = {p:true} if -p option is on
	*/
	mkdir: function(folder, config){
		
		var self = this;
		return new Promise(function(resolve, reject){
			folder = Session.formatInput(folder);
			if(typeof folder !== "string" || (config && typeof config !== "object")){
				reject('invalid input');
				return;
			}
			
			var promise;
			if(self.method === 'GET'){
				var url = self.preurl + self.pwd + 'mkdir ' + Session.parseConfig(config) + folder;
				promise = Session.ajax(self.method, encodeURI(url));
			}
			else if(self.method === 'POST'){
				var url = self.preurl, data = { command: Session.spliceVoid(['mkdir', Session.parseConfig(config), folder]), path:self.pwd.slice(1,-1) };
				promise = Session.ajax(self.method, url, JSON.stringify(data));
			}
			
			promise.then(function(res){
				if(res.status == "OK")
					resolve();
				else
					reject(Error(res));
			});
			
			promise.catch(function(code){
				reject(Error("Unknown error: HTTP status " + code));
			});
		});
	},
	/*
		ls
		set config ={a:true, l:true} if -al option is on
	*/
	ls: function(folder, config){
		
		var self = this;
		return new Promise(function(resolve, reject){
			folder = Session.formatInput(folder);
			if(config && typeof config !== "object"){
				reject('invalid input');
				return;
			}
			
			folder = folder || "";
			config = config || {a:false, l:false};
			
			var promise;
			if(self.method === 'GET'){
				var url = self.preurl + self.pwd + 'ls ' + Session.parseConfig(config) + folder;
				promise = Session.ajax(self.method, url);
			}
			else if(self.method === 'POST'){
				var url = self.preurl + '/', data = { command: Session.spliceVoid(['ls', Session.parseConfig(config), folder]), path: self.pwd.slice(1,-1) || '/'};
				promise = Session.ajax(self.method, url, JSON.stringify(data));
			}
			
			promise.then(function(res){
				if(res.status == "OK")
					resolve(res.msg);
				else
					resolve(Error(res.meg));
			});
			
			promise.catch(function(code){
				reject(Error("Unknown error: HTTP status " + code));
			});
		});
	},
	/*
		rm
		set config = {r:true} if -r option is on
	*/
	rm: function(file, config){
		
		var self = this;
		return new Promise(function(resolve, reject){
			file = Session.formatInput(file);
			if(typeof file !== "string" || (config && typeof config !== "object")){
				reject('invalid input');
				return;
			}
			
			var promise;
			if(self.method === 'GET'){
				var url = self.preurl + self.pwd + 'rm ' + Session.parseConfig(config) + file;
				promise = Session.ajax(self.method, url);
			}
			else if(self.method === 'POST'){
				var url = self.preurl, data = { command: Session.spliceVoid(['rm', Session.parseConfig(config), file]), path: self.pwd.slice(1,-1) };
				promise = Session.ajax(self.method, url, JSON.stringify(data));
			}
			
			promise.then(function(res){
				if(res.status == "OK")
					resolve();
				else
					reject(Error(res));
			});
			
			promise.catch(function(code){
				reject(Error("Unknown error: HTTP status " + code));
			});
		});
	},
	chown : function(owner, group, file, config){
		var self = this;
		return new Promise(function(resolve, reject){
			file = Session.formatInput(file);
		
			if(!file){
				reject('unspecific file.'); 
				return;
			}
		
			owner = owner || "";
			group = group || "";
		
			if(typeof owner !== 'string' ||
			   typeof group !== 'string' ||
			   typeof file !== 'string' ||
		       (config && typeof config !== 'object')){
					reject('invalid input.');
					return;
			}
				
			var promise;
			if(method === 'GET'){
				var url = self.preurl + self.pwd + 'chown ' + Session.parseConfig(config) + owner + ':' + group + file;
				promise = Session.ajax(self.method, url);
			}
			else if(method === 'POST'){
				var url = self.preurl, data = { command: Session.spliceVoid(['chown', Session.parseConfig(config), owner + ':' + group, file]), path: self.pwd.slice(1,-1) };
				promise = Session.ajax(self.method, url, JSON.stringify(data));
			}
			
			promise.then(function(res){
				if(res.status == "OK")
					resolve();
				else
					reject(Error(res));
			});
			
			promise.catch(function(code){
				reject(Error("Unknown error: HTTP status " + code));
			});
		});
	},
	chmod : function(mode, file, config){
		var self = this;
		return new Promise(function(resolve, reject){
			file = Session.formatInput(file);
		
			if(!file)
				reject('unspecific file.'); 
		
			if(typeof mode !== 'string' ||
			   typeof file !== 'string' ||
		       (config && typeof config !== 'object'))
					reject('invalid input.');
				
			var promise;
			if(method === 'GET'){
				var url = self.preurl + self.pwd + 'chmod ' + Session.parseConfig(config) + mode + file;
				promise = Session.ajax(self.method, url);
			}
			else if(method === 'POST'){
				var url = self.preurl, data = { command: Session.spliceVoid(['chmod', Session.parseConfig(config), mode, file]), path: self.pwd.slice(1,-1) };
				promise = Session.ajax(self.method, url, JSON.stringify(data));
			}
			
			promise.then(function(res){
				if(res.status == "OK")
					resolve();
				else
					reject(Error(res));
			});
			
			promise.catch(function(code){
				reject(Error("Unknown error: HTTP status " + code));
			});
		});
	}
}
