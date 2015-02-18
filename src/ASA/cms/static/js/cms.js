function Session(username){
	if(typeof username !== "string")
		throw TypeError();
	
	Session.extend(this,{
		username: username,
		host: location.hostname,
		preurl: '/cms',
		pwd: "/",
	});
}

Session.extend = function(des, src){
	for(var i in src)
		des[i] = src[i];
}

Session.debugMode = true;

Session.ajax = function(path){
	var self = this;
	return new Promise(function(resolve,reject){
		var req = new XMLHttpRequest();
		
		req.onreadystatechange = function(){
			if(req.readyState == 4){
				if(self.debugMode){
					console.log(path);
					console.log(req.status + ':' + req.response);
				}
				
				if(req.status == 200)
					resolve(JSON.parse(req.response));
				else
					reject(req.status);
			}
		}
		
		req.open("GET", path, true);
		req.send(null);
	});
};

Session.parseConfig = function(config){
		var str = "";
		for(var i in config)
			if(config[i])
				str += '-' + i + ' ';
		return str;
	},

Session.prototype = {
	constructor: Session,
	cd: function(folder){
		if(typeof folder !== "string") throw TypeError();
		var self = this;
		return new Promise(function(resolve, reject){
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
		
			url = self.preurl + self.pwd + 'cd ' + folder;
			
			var promise = Session.ajax(encodeURI(url));
			
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
		if(typeof folder !== "string" || (config && typeof config !== "object"))
			throw TypeError();
		var self = this;
		return new Promise(function(resolve, reject){
			config = config || {p:false};
			
			var url = self.preurl + self.pwd + 'mkdir ' + Session.parseConfig(config) + folder;
			
			var promise = Session.ajax(encodeURI(url));
			
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
		if(config && typeof config !== "object")
			throw TypeError();
		var self = this;
		return new Promise(function(resolve, reject){
			folder = folder || "";
			config = config || {a:false, l:false};
	
			var url = self.preurl + self.pwd + 'ls ' + Session.parseConfig(config) + folder;
			
			var promise = Session.ajax(url);
			
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
		if(typeof file !== "string" || (config && typeof config !== "object"))
			throw TypeError();
		var self = this;
		return new Promise(function(resolve, reject){
			config = config || {r:false};
			
			var url = self.preurl + self.pwd + 'rm ' + Session.parseConfig(config) + file;
			
			var promise = Session.ajax(url);
			
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
