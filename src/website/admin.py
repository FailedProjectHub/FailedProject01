from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(SessionUploaderRecord)
admin.site.register(VideoFileAttrib)


for cls in BasePerInfoMetaclass.Register.values():
    try:
        admin.site.register(cls)
    except:
        pass
