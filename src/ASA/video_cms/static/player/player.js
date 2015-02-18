function render_player(token, callbacks){	
	// construct player
	var inst = ABP.create(document.getElementById("player"),{
		"src":{
			"playlist":[
				{
					"sources":{"video/mp4":"/download/"+token},
				},
			],
		},
		"width":1280,
		"height":640
	});
    var owner = token;
    var cm = inst.cmManager;
	// load danmaku
	$.get("/danmaku/"+token, function(data, status) {
        if (status!="success") {
            console.log("Network Error: "+status);
            return;
        }
        console.log(data);
        var res = eval(data);
        var cdata = new Array();
        for (var i=0;i<res.length;++i) {
            inst.dminsert(new CoreComment(cm, res[i]));
        }
    });


	if (typeof io != "undefined") {
		// websocket
		var socket = new io.connect("http:\/\/" + window.location.hostname + ":4000/");

		// enter channel
		socket.emit("enter_channel", token);
		//subscribe live danmaku
		socket.on("live_danmaku", function(danmaku){
				console.log(danmaku);
				inst.dminsert(danmaku);
		});
		inst.addListener("senddanmaku",function(dm){
			if (inst.playing) {
				inst.dmsend(dm);
				setTimeout(function(){socket.emit("send_danmaku", dm);}, 1000);
			} else socket.emit("send_danmaku", dm);
		});
	}
    
    
    

    //inst.scripting = true;
    

    if (callbacks != null)
        callbacks()
}

