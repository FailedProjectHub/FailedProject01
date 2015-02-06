CMS由两个部分组成：用户系统，文件系统

=====================================
1.文件系统:

    大概是做成unix-like的那样
    /
        home
        public
        files

    /home 同unix-like的home一样，会存放所用用户的名字对应的
    文件夹，这些目录下会含有该用户上传的视频，可以有子目录，
    可以嵌套

    /public 下是显示在视频站上的结构。同样的,可以有子目录，
    可嵌套

    /files 这一部分其实是CDN-director在CMS的API，通过视频的
    token返回几个可用的URL

    逻辑视频文件使用引用计数规则（如果一个逻辑视频文件没有在
    任何文件夹里面存在，则会被删除，同时对CDN-director发出
    删除指令)
    
    文件以及文件夹使用ACL(access control list)规则进行权限管理

=====================================
2.用户系统:

	参照linux(with)
		    	
======================================
另外之一:

	实现部分POSIX的权限接口(例如chmod). 而对于ls, cd, mkdir暂不实现POSIX接口.
	
========================================
另外之二:
	
	视频从上传完视频到审核再到放到视频站过程
	需要反复说明的几点：
		1./public下的文件夹直接对应到视频站的分类，所以文件被连接到/public/xxxxx下就表示审核通过，可以被任何用户看到
		2./public下的文件夹实际上是一个group, group super host就是版主, group host是副版主
		3.在逻辑组织中有一个group叫做all,所有用户(如果没有注册就是ip作为用户名)都在这个group里面.还有一个group叫做ASAer，所有注册用户都在这里面.
		4./public/xxxxx和/public/xxxxx下的所有文件的read_by_group都含有all
		5./public/xxxxx会对应一个/home/xxxxx_upload,/home/xxxxx_upload的
		created_by_group都有ASAer,同时/public/xxxxx的group host(super host)
		也是/home/xxxxx_upload的group host(super host)
		/
			home/
				xxxxx_upload
					group host: a0,a1,...an
					group super host: b
				...
			public/
				xxxxx
					group host: a0,a1,...an
					group super host: b
					(the same as /home/xxxxx_upload/)
				...
			

	下面开始介绍过程：
		1.用户上传文件到/home/xxxxx_upload
		2.group admin(super admin)看到视频，审核
		3.审核通过，admin把文件移动到/public/xxxxx,并把原来在/home/xxxxx_upload的文件删除
		
======================================
另外之三:
	
	与前端的交互
	{{hostname}}/cms/<path>/<operation>
	GET operation:
		ls: 查看当前文件架(对该用户可见的)的所有信息.如果是一个视频文件则返回错误操作
		ls <filename>: 返回这个文件的具体信息,如果是一个未上传完全的文件则response会包括已上传和未上传chunk的信息
		rm <filename>: 删除当前文件(对该用户可见并可删除).如果是一个文件夹则需要"rm -r <foldername>"
		get_url <filename>: 获得可以获得当前视频文件流的url
		cp <filepath_a> <filepath_a>: 把file_a复制一份到filepath_b
		mv <filepath_a> <filepath_b>: *剪切
		mkdir <foldername>:建立一个文件夹 
		cd <path>
	POST operation:
		init <filename>: 创建一个文件	(需要权限),发送一个描述文件信息的json
		finish <filename>: 完成一个文件上传
	PUT operation:
		put <filename> <chunk_no>:
			上传文件<filename>的第<chunk_no>个chunk
	
=====================================
另外之四:

	后端布置
	urls.py正则表达式匹配{{hostname}}/cms/<path>/<operation>
	根据操作名调用cms.plugin内的process函数
	规定对于操作的接口
	def process(environ, args)
	environ是一个字典对象, 现在已经规定的key-value为: "path":str, "username":str, "user":user(django自带的auth中的user对象)
	args命令参数，举例: mkdir -p /home/voidrank 命令，会调用../plugins/mkdir.py,传入参数为["-p","/home/voidrank"]
	user是当前用户的信息
	
======================================
另外之五:

	文件模型。所有的文件都有一个basefile。所有的basefile都会被反向连接一个OneToOneField, 被称之为属性（应要求每个File只有一种属性）