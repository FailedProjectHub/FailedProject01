var Uploader;
(function(){
	Uploader = function(file, onStatusChange){
		if (typeof onStatusChange != "function") onStatusChange=function(obj){};
		var config = {
			"chunksize":    65536,
			"url"     :     window.location.origin+"/",
			"filename":		"test_file",
		};
		/* get filename from full path */
		function getFileName(path) {
			var pos1 = path.lastIndexOf('/');
			var pos2 = path.lastIndexOf('\\');
			var pos = Math.max(pos1, pos2);
			if (pos==0&&path[0]!='/'&&path[0]!='\\') return path;
			else return path.substring(pos+1);
		}

		/* make ajax */
		function ajax(method, url, data, headers) {
			if (typeof data == "undefined") data=null;
			if (typeof headers == "undefined") headers={};
			return new Promise(function(resolv, reject){
				var xhr=new XMLHttpRequest();
				xhr.onreadystatechange=function() {
					if (xhr.readyState==4) {
						if (xhr.status>0 && xhr.status<400) {
							resolv(xhr.responseText);
						} else {
							reject(Error(xhr.responseText));
						}
					}
				};
				xhr.open(method, url, true);
				for (var i in headers) {
					xhr.setRequestHeader(i,headers[i]);
				}
				xhr.send(data);
			});
		}
		/* parse json */
		var parseJSON = function(json){return eval('('+json+')');};
		
		/* init vars */
		var obj=this;
		
		config.filename=getFileName(document.getElementById("file").value); 
		var token;

		var seqnow=0;
		var seqs=parseInt(file.size/config.chunksize);

		var chunksize = config["chunksize"];
		var pos=0;
		var reader = new FileReader(); 

		var checksumchunk = 65536;

		var sum;
		
		var checksumprog=0;
		var uploadprog=0;
		onStatusChange(obj);
		/* init promise */
		var chain = new Promise(function(resolv,reject){sha256_init();resolv(0);});
		/* calculate sha256sum */
		for (var p=0;p<parseInt((file.size-1)/checksumchunk+1);p++) {
			chain = chain.then(function(pos) {
				return new Promise(function(resolve, reject) {
					var thischunk = pos+checksumchunk<file.size?checksumchunk:file.size-pos;
					reader.onload=function() {
						checksumprog=pos/file.size*100;
						onStatusChange(obj);
						sha256_update(this.result, thischunk);
						resolve(pos+thischunk);
					};
					reader.readAsBinaryString(file.slice(pos, pos+thischunk));
				});
			});
		}
		/* finalize sha256sum */
		chain = chain.then(function(){
			sha256_final();
			sum=sha256_encode_hex();
			checksumprog=100;
			onStatusChange(obj);
		})
		/* get token from sessions && return last seq */
		.then(function(){return ajax("GET", config.url+"upload/session/");})
		.then(parseJSON)
		.then(function(sessions){
			var f=0;
			for (;f<sessions.length;f++) {
				if (sessions[f].hash == sum) break;
			}
			if (f>=sessions.length) {
				return ajax("POST", config.url+"upload/init/", '{"size":'+file.size+',"hash":"'+sum+'","filename":"'+config.filename+'","chunksize":'+config.chunksize+'}')
				.then(parseJSON)
				.then(function(res){token=res.token;return 0;})
			} else {
				token=sessions[f].token;
				return ajax("GET", config.url+"upload/chunk/"+token)
				.then(parseJSON)
				.then(function(res) {
					var list=[];
					for (var i=0;i<seqs;i++) list[i]=false;
					for (var i=0;i<res.length;i++) {
						list[res[i].seq]=true;
					}
					seqnow=seqs;
					for (var i=0;i<seqs;i++) if (!list[i]) {seqnow=i;break;}
					return seqnow;
				});
			}
		});
		/* upload chunks */
		for (var i=seqnow;i<seqs;i++) {
			chain = chain.then(function(seq) {
				return new Promise(function(resolv,reject){
					var offset=config.chunksize*seq;
					var chunksize=offset+config.chunksize*2<=file.size?config.chunksize:file.size-offset;
					console.log("chunk: "+seq+" "+offset+" "+chunksize+" "+offset+chunksize);
					var reader = new FileReader();
					reader.onload=function(e) {
						onStatusChange(obj);
						var data = String.fromCharCode.apply(null, new Uint8Array(this.result));
						var hash=sha256_digest(data);
						ajax("PUT", config.url+"upload/chunk/"+token+"/?hash="+hash+"&seq="+seq, this.result, {
							"Content-Type": "application/x-www-form-urlencoded"
						}).then(function(m){
							uploadprog = offset*100/file.size;
							onStatusChange(obj);
							//console.log(m);
						}).then(function(){resolv(seq+1)});
					};
					reader.readAsArrayBuffer(file.slice(offset, offset+chunksize));
				});
			});
		}
		/* finish upload */
		chain = chain.then(function(seq) {
			uploadprog = 100;
			onStatusChange(obj);
			return ajax("GET", config.url+"upload/store/"+token);
		})
		.then(function(m){console.log(m);})
		.catch(function(e){
			console.log(e);
			onStatusChange(obj);
		});
		Object.defineProperty(this, "checksumprog", {
			get: function() {return checksumprog;}
		});
		Object.defineProperty(this, "checksum", {
			get: function() {return sum;}
		});
		Object.defineProperty(this, "uploadprog", {
			get: function() {return uploadprog;}
		});
	};

})();
