
import requests
from django.conf import settings

from django.http.response import HttpResponse
import json



def send_to_firebase(data):
    key = "key=%s"%settings.FIREBASE_SERVER_KEY
    #import pdb;pdb.set_trace()
    request=requests.post(settings.BASE_GCM,
                          headers={'Authorization':key,'Content-Type':"application/json"},
                          data=json.dumps(data, separators=(',', ':'), sort_keys=True).encode('utf8'))

    #request.json()


class HttpJSONResponse(HttpResponse):
    def __init__(self, data, name=None,*args, **kwargs):
        from django.core.serializers.json import DjangoJSONEncoder

        if name:

            serialized = kwargs.pop('serialized', False)


            kwargs['content_type'] = 'application/json'

            kwargs['X-Accel-Redirect'] = '/json/'
            kwargs['Content-Disposition'] = 'attachment; filename=%s.pdf' % (name, )

            super(HttpJSONResponse, self).__init__(*args, **kwargs)
        else:
            serialized = kwargs.pop('serialized', False)
            if not serialized:
                data_json = json.dumps(data,cls=DjangoJSONEncoder)
            else:
                data_json=data

            kwargs['content_type'] = 'application/json'
            super(HttpJSONResponse, self).__init__(data_json, *args, **kwargs)