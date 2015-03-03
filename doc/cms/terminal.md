API

	GET: {{hostname}}/cms/<path>/<command> (将在released 版本中删除)
	POST: (推荐)
		content为一个json:
		{
			command: array,
			path: str
		}
		解释：command如何修改成array的形式.例如"rm -r 123"转成['rm', '-r', '123'],
			即为用连续的空格作为一个分隔符，把字符串分成几个字符串，然后组成一个array.
	
	现在已有的一些plugin:
		ls, rm, chown, chmod, mkdir, cd

