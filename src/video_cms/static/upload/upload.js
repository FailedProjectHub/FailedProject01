var Uploader;
(function(){
	Uploader = function(file, onStatusChange, callback){
		Object.defineProperty(this, "checksumprog", {
			get: function() {return checksumprog;}
		});
		Object.defineProperty(this, "checksum", {
			get: function() {return sum;}
		});
		Object.defineProperty(this, "uploadprog", {
			get: function() {return uploadprog;}
		});
		if (typeof onStatusChange != "function") onStatusChange=function(obj){};
    if (typeof callback != "function") callback=function(){};
		var config = {
			"chunksize":    65536, /* min=65536, max=??? */
			"url"     :     window.location.origin+"/",
			"filename":		"test_file",
		};

		/* make ajax */
		function ajax(method, url, data, headers) {
			if (typeof data == "undefined") data=null;
			if (typeof headers == "undefined") headers={};
			return new Promise(function(resolve, reject){
				var xhr=new XMLHttpRequest();
				xhr.onreadystatechange=function() {
					if (xhr.readyState==4) {
						if (xhr.status>0 && xhr.status<400) {
							resolve(xhr.responseText);
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
		
		config.filename=file.name; 
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
		sha256_init();
		/* init promise */
		var chain = Promise.resolve(0);
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
				if (sessions[f].chunksize) config.chunksize=sessions[f].chunksize;
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
		})
		/* upload chunks */
		.then(function(seqnow){
			var upchain = Promise.resolve(seqnow);
			for (var i=seqnow;i<seqs;i++) {
				upchain = upchain.then(function(seq) {
					return new Promise(function(resolve, reject){
						var offset=config.chunksize*seq;
						var chunksize=offset+config.chunksize*2<=file.size?config.chunksize:file.size-offset;
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
							}).then(function(){resolve(seq+1)});
						};
						reader.readAsArrayBuffer(file.slice(offset, offset+chunksize));
					});
				});
			}
			return upchain;
		})
		/* finish upload */
		.then(function(seq) {
			uploadprog = 100;
			onStatusChange(obj);
			return ajax("GET", config.url+"upload/store/"+token);
		})
    .then(parseJSON)
		.then(function(m){
      console.log(m);
      callback(m);
    });
    /*
		.catch(function(e){
			console.log(e);
			onStatusChange(obj);
		});
    */
	};

})();
