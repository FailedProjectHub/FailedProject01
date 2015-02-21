from . import models
from django.forms import ModelForm


class PerInfoFormMetaclass(type(ModelForm)):
    Register = {}

    def __init__(cls, name, bases, nmspc):
        super(PerInfoFormMetaclass, cls).__init__(name, bases, nmspc)
        PerInfoFormMetaclass.Register[name.lower()] = cls


Register = PerInfoFormMetaclass.Register


class GenericPerInfo(ModelForm, metaclass=PerInfoFormMetaclass):
    class Meta:
        model = models.GenericPerInfo
        fields = ['avatar', 'email']
