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

Session.parseConfig = function(config){
		var str = "";
		for(var i in config)
			if(config[i]){
				if(!str)
					str = '-';
				str += i;
			}
		return str;
}

Session.formatInput = function(str){
	while(str && str[0] === '/')
		str = str.slice(1);
	while(str && str[str.length-1] === '/')
		str.length --;
	return str;
}

Session.prototype = {
	constructor: Session,
	send: function(com){
		//erase extra space
		com = com.replace(/^ +/, '');
		com = com.replace(/ +$/, '');
		//merge multiple space
		com = com.replace(/ +/, ' ');
		
		var promise;
		if(this.method === 'GET'){
			var url = this.preurl + this.pwd + com;
			promise = Session.ajax(this.method, encodeURI(url)); 
		}
		else if(this.method === 'POST'){
			var url = this.posturl, data = { command: com.split(/ +/), path: this.pwd.slice(0,-1) || '/'};
			promise = Session.ajax(this.method, encodeURI(url), JSON.stringify(data));
		}
	
		return promise;
	},
	cd: function(config, folder){
		
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
			
			var promise = self.send('cd ' + folder);
			
			promise.then(function(res){
				if(res.status == "OK"){
					self.pwd += folder + '/';
					resolve();
				}
				else
					reject(res.msg);
			});
			
			promise.catch(function(code){
				reject("Unknown error: HTTP status " + code);
			});
		});
	},
	/*
		mkdir
		set config = {p:true} if -p option is on
	*/
	mkdir: function(config, folder){
		
		var self = this;
		return new Promise(function(resolve, reject){
			folder = Session.formatInput(folder);
			if(typeof folder !== "string" || (config && typeof config !== "object")){
				reject('invalid input');
				return;
			}
			
			var promise = self.send('mkdir ' + Session.parseConfig(config) + ' ' + folder);
			
			promise.then(function(res){
				if(res.status == "OK")
					resolve();
				else
					reject(res.msg);
			});
			
			promise.catch(function(code){
				reject("Unknown error: HTTP status " + code);
			});
		});
	},
	/*
		ls
		set config ={a:true, l:true} if -al option is on
	*/
	ls: function(config, folder){
		
		var self = this;
		return new Promise(function(resolve, reject){
			folder = Session.formatInput(folder);
			if(config && typeof config !== "object"){
				reject('invalid input');
				return;
			}
			
			folder = folder || "";
			config = config || {a:false, l:false};
			
			var promise = self.send('ls ' + Session.parseConfig(config) + ' ' + folder);
			
			promise.then(function(res){
				if(res.status == "OK")
					resolve(res.msg);
				else
					reject(res.msg);
			});
			
			promise.catch(function(code){
				reject("Unknown error: HTTP status " + code);
			});
		});
	},
	/*
		rm
		set config = {r:true} if -r option is on
	*/
	rm: function(config, file){
		
		var self = this;
		return new Promise(function(resolve, reject){
			file = Session.formatInput(file);
			if(typeof file !== "string" || (config && typeof config !== "object")){
				reject('invalid input');
				return;
			}
			
			var promise = self.send('rm ' + Session.parseConfig(config) + ' ' + file);
			
			promise.then(function(res){
				if(res.status == "OK")
					resolve();
				else
					reject(res.msg);
			});
			
			promise.catch(function(code){
				reject("Unknown error: HTTP status " + code);
			});
		});
	},
	chown : function(config, owner, group, file){
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
				
			var promise = self.send('chown ' + Session.parseConfig(config) + ' ' + owner + ':' + group + ' ' + file);
			
			promise.then(function(res){
				if(res.status == "OK")
					resolve();
				else
					reject(res.msg);
			});
			
			promise.catch(function(code){
				reject("Unknown error: HTTP status " + code);
			});
		});
	},
	chmod : function(config, mode, file){
		var self = this;
		return new Promise(function(resolve, reject){
			file = Session.formatInput(file);
		
			if(!file)
				reject('unspecific file.'); 
		
			if(typeof mode !== 'string' ||
			   typeof file !== 'string' ||
		       (config && typeof config !== 'object'))
					reject('invalid input.');
				
			var promise = self.send('chmod ' + Session.parseConfig(config) + ' ' + mode + ' ' + file);
			
			promise.then(function(res){
				if(res.status == "OK")
					resolve();
				else
					reject(res.msg);
			});
			
			promise.catch(function(code){
				reject("Unknown error: HTTP status " + code);
			});
		});
	}
}
