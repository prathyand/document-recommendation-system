# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from recomapiservice.models import Recom
from recomapiservice.serializers import RecomSerializer
import urllib.request
from urllib import parse
import json
from django.http import HttpResponse


class SimilardocListView(APIView,
                    UpdateModelMixin,
                    DestroyModelMixin):

    def get(self, request,docid):
        urlData = "http://recengineservice:8002/similardoc/?docid="
        urlData = urlData + parse.quote(docid)
        webURL = urllib.request.urlopen(urlData)
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        resp = json.loads(data.decode(encoding))
        clauses = ' '.join(['''WHEN %s THEN %s''' % ("'"+pk+"'", i) for i, pk in enumerate(resp["Resultkeys"])])
        ordering = 'CASE keyid %s END' % clauses
        try:
            queryset = Recom.objects.filter(pk__in=resp["Resultkeys"]).extra(select={'ordering': ordering}, order_by=('ordering',))
        except Recom.DoesNotExist:

            return Response({'errors': 'item does not exist.'}, status=400)

        read_serializer = RecomSerializer(queryset,many=True)

        return Response(read_serializer.data)



