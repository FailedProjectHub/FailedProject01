I#Command-line-API for cms

##概述


cms采用unix-like的命令操作。操作时，需要向服务器发送一个GET请求，请求的url格式如下

	/cms/{{path}}/{{command}} 

**注意：请对url中出现的空格等字符进行转义**

例如 `GET /cms/ASA.tv/mydir/mkdir%20-p ` 将请求服务器在ASA.tv目录下创建名为mydir的文件夹

后端匹配url的正则表达式如下(python语法)

	^cms/(?P<path>(([a-z0-9A-Z-_]+/)*))(?P<command>([a-z0-9A-Z-_ /.])+)$
	
任何不匹配该模式串的url将返回错误

前端遇到错误会有两种情况：第一种情况就是response.content不是json，不可解析，那么应该terminal显示“unknown error”, 如果该plugin对于这种情况有其他的处理，则把这部分的处理留给该plugin的前端部分来呈现。第二种情况则是response.content是一个json，可以解析，但是返回了{'status':'error', 'msg':'str'}，那么应该显示str的部分。
我们称第一种错误为未知错误，第二种为正常错误。

匹配该模式串的url将被服务器接收，并返回一个JSON。

一个被接收的命令存在四种可能的结果

1. 命令执行目录(path)不存在
2. 命令不存在或不合法
3. 命令合法但因为权限等原因操作失败
4. 命令合法且操作成功
I
四种错误都为正常错误，前端不需要了解期中的逻辑，只需要按照正常错误的显示格式显示即可。

##命令

### cd

检验path指向的文件（夹）是否存在

__返回__

	文件（夹）存在:{"msg":"OK"} (*需要区分文件和文件夹*）
	不存在:{"msg":"{{path}}"}，这里path表示第一个不存在的folder

---------------------------------------
### mkdir [-p]

创建path指向的文件(夹?)
(*-p需要显式添加到mkdir后吗*)

__返回__

	创建成功：
	创建失败：

---------------------------------------
### rm [-r]

删除path指向的文件（夹)

__返回__

	删除成功：
	删除失败：

---------------------------------------
### ls path


option:  

-R --recursive 只有admin权限的用户才可使用,返回path下所有文件的信息
 
--sort=attirb attrib是一个字符串，相当于File.objects.order_by(attrib)

-r 当制定了--sort后才会生效，表示反向返回结果

--op=a,  --ed=b : 显示从序号从op到ed的文件

-l 每行指列出一个文件

--display=attrib, 展示的属性，同--sort一样是一个字符串(当-l存在是才有)

打印path指向的目录下的文件（夹），同unix-like系统的操作

__返回__

	查询失败：{"status": "error", "msg": "{{reason}}"}
	查询成功：{"status": "OK", "msg": {{msg}}}	
	msg的格式
		[[第一行的信息], [第二行的信息], ...]
	例如:
		[[object_a1, object_a2 ...], [object_b1, object_b2, ...] ...]
		在terminal上应该显示为:
			object_a1 object_a2 ...
			object_b1 object_b2 ...
			...


----------------------------------------

