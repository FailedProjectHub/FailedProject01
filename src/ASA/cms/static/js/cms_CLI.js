$(function() {
	var session = new Session('ASA.tv');
	var jqconsole = $('#console').jqconsole('Log in @' + session.host + 'as ' + session.username + '\n',
											session.username + '@' + session.host + ':' + session.pwd + ' >>> '	);
	
	var stringify = {
		ls: function(o){
			var str = '';
			for(var i = 0; i < o.length; i++){
				for(var j = 0; j < o[i].length; j++)
					str += o[i][j] + ' ';
				str += '\n';
			}
			//if(str.length) str.length--;
			return str;
		},
	}, configParser = function(str){
		var o = {};
		str = str.split(/ +/);
		
		for(var i = 1; i < str.length; i++)
			if(str[i][0] === '-')
				for(var j = 1; j < str[i].length; j++)
					o[str[i][j]] = true;
		
		return o;
	}, errorHandler = {
		ls: function(path){
			return path + " does not exist.\n";
		},
		unknown: function(){
			return 'encountered an unknown error.\n';
		}
	};
	
    var prompt = function() {
        jqconsole.Prompt(true, function (input) {
			jqconsole.prompt_label_main = session.username + '@' + session.host + ':' + session.pwd + ' >>> ';
			input = input.replace(/^ */, "");
			var config = configParser(input);
			var com = input.split(' ')[0];
			input = input.replace(/-\w*/, '');
			var argv = input.split(/ +/)[1];
			
			var next = function(text){
				if(text)
					jqconsole.Write(text, 'jqconsole-output');
				prompt();
			}
			
			if(!session[com])
				next('No such command.\n');
			else{
				var promise = session[com](argv, config);
				
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
						next(errorHandler.unknown());
				});
			}
        });
    };
    prompt();
});
