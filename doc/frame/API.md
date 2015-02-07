ICommand-line-API
===========================

用正则表达式来匹配url:

	^cms/(?P<path>(([a-z0-9A-Z-_]+/)*))(?P<command>([a-z0-9A-Z-_ /.])+)$
	

* cd 如果成功后台会以json的消息返回{"msg":"OK"}(后台只会告诉你这个文件存在不存在)，如果失败，后台会返回{"msg":"{{path}}"}，期中path表示第一个不存在的folder
* mkdir [-p] 创建文件，基本同unix-like系统的操作
* rm [-r] 删除文件，基本同unix-like系统的操作
* ls 同unix-like系统的操作，返回值"msg":["{{path1}}", "{{path2}}", ...]

返回值json: 
	
	错误{"status": "error", "msg": "{{reason}}"}
	正常返回{"status": "OK", "msg": {{msg}}}	
	msg的格式
		[[第一行的信息], [第二行的信息], ...]
	例如:
		[[object_a1, object_a2 ...], [object_b1, object_b2, ...] ...]
		在terminal上应该显示为:
			object_a1 object_a2 ...
			object_b1 object_b2 ...
			...



