from django.contrib import admin
from .models import *

# Register your models here.


for cls in BasePerInfoMetaclass.Register.values():
    try:
        admin.site.register(cls)
    except:
        pass
