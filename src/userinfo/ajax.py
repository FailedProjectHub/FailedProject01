# from django.db.models.fields import Field
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import BasePerInfoMetaclass

try:
    import simplejson as json
except:
    import json


@login_required
def PerInfoAJAX(request, infotype):
    modeltype = BasePerInfoMetaclass.Register[infotype]
    model = modeltype.objects.get(user=request.user)
    return HttpResponse(json.dumps(model.as_dict()))
