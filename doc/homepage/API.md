----------------------------------------------
register.html

GET {{hostname}}/register/  
response register.html

注册必要信息  
username  
passwd  
email  

放到一个form里头转成json发给服务器  
POST {{hostname}}/register/  
注册成功则返回
{"status":"OK"}

检查username是否重复  
GET {{hostname}}/register/check_id/{{username}}  
response json   
{"status":"OK"}表示该id没有注册   
{"status":"duplicated"}表示该id已被注册



-----------------------------------------------

homepage.html

GET {{hostname}}/homepage/  
response register.html

左边应该有几个按钮:  
基本信息  
高级设定信息  
系统记录信息  
社交信息  
投稿信息  

通过ajax渲染右边内容  

不可修改的基本信息  
GET {{hostname}}/homepage/genericperinfo  
{
	"username": str,
	"email": str
	"avatar": url
}

高级设定信息  
GET {{hostname}}/homepage/advancedperinfo/  
{
	chunksize: int
}

POST {{hostname}}/homepage/advacedperinfo/  
格式同GET


修改密码   
POST  {{hostname}}/homepage/passwd/  
{
	oldpasswd: str,
	newpasswd: str
}

投稿信息  
GET {{hostname}}/homepage/myupload/?op=0&ed=9  
op,ed分别是显示的自己上传的视频的序号（按照上传时间降序返回）  
response [ [rec号(int), 缩略图的url(str)], ... ]  
如果不够的话就返回到最后一个为止

朋友信息  
GET {{hostname}}/homepage/myfriends/?op=0&ed=9  
response [ friendname0, friendname1, ...]

社团信息
GET {{hostname}}/homepage/mygroup/
response [ group0, group1, group2 ...]

获取头像
GET {{hostname}}/homepage/avatar/
得到头像

=====================================
关于response

非正常返回 
{
	"status": "error",
	"msg": reason
}

正常返回
{
	"status": "OK"
}