function render_player(token, callbacks){
    // websocket
    var socket = new io.connect("http:\/\/" + window.location.hostname + ":4000/");
    var owner = token;

    // enter channel
    socket.emit("enter_channel", token);

    
    $.get("/danmaku/"+token, function(data, status) {
        if (status!="success") {
            console.log("Network Error: "+status);
            return;
        }
        var res = eval(data);
        var cdata = new Array();
        for (var i=0;i<res.length;++i) {
            cdata.push(new CoreComment(cm, res[i]));
        }
        cm.load(cdata);
    });

    //subscribe live danmaku
    socket.on("live_danmaku", function(danmaku){
            console.log(danmaku);
            cm.insert(danmaku);
    });

    inst.scripting = true;
    inst.cmManager.start();
    var cm = inst.cmManager;
    $(inst.txtText).keyup(function(event){
        if( event.which === 13){

            var danmaku={
                "owner": owner,
                "mode": 1,
                "stime": parseInt(inst.video.currentTime*1000),//to prevent dm not showing
                "text": $(inst.txtText).val(),
                "cindex": 0,
                "motion": [],
                "size": 25,
                "color": 0xffffff,
            };
            cm.send(danmaku);
            socket.emit("send_danmaku", danmaku);

            $(inst.txtText).val("");
        }
    });

    if (callbacks != null)
        callbacks()
}

