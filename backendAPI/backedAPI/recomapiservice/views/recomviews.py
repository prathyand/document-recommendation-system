# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
import urllib.request
from urllib import parse
from datetime import datetime
import json

from recomapiservice.models import Recom
from recomapiservice.serializers import RecomSerializer

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count':self.page.paginator.count,
            'currentpage': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class RecomListView(APIView,
                    UpdateModelMixin,
                    DestroyModelMixin,CustomPagination):

    def get(self, request,keyid=None):
        # keyid=request.query_params.get('keyid', None)

        if keyid:
            try:
                queryset = Recom.objects.get(keyid=keyid)

            except Recom.DoesNotExist:

                return Response({'errors': 'item does not exist.'}, status=400)

            read_serializer = RecomSerializer(queryset)

            return Response(read_serializer.data)

        else:
            if request.GET.get('updaterecom'):
                # Trigger update
                urlData = "http://recengineservice:8002/triggerupdate/?trigger=1"
                # urlData = urlData + parse.quote(docid)
                webURL = urllib.request.urlopen(urlData)
                data = webURL.read()
                encoding = webURL.info().get_content_charset('utf-8')
                resp = json.loads(data.decode(encoding))
                print("from recom update ",resp)

            queryset = Recom.objects.all().order_by('-snooze_priority','-score')
            queryset = self.paginate_queryset(queryset, request, view=self)
            read_serializer = RecomSerializer(queryset, many=True)
        # Return a HTTP response object with the list
        return self.get_paginated_response(read_serializer.data)

    def put(self, request,keyid=None):
        # keyid=request.query_params.get('keyid', None)
        try:
            # Check if the  item exists
            rec_item = Recom.objects.get(keyid=keyid)
        except Recom.DoesNotExist:
            # return an error response
            return Response({'errors': 'item does not exist.'}, status=400)

        # use the serializer to validate the updated data
        update_serializer = RecomSerializer(rec_item, data=request.data)

        # proceed to saving data to the database
        if update_serializer.is_valid():

            # update the item in the database
            recom_item_object = update_serializer.save()

            # Serialize the item from Python object to JSON format
            read_serializer = RecomSerializer(recom_item_object)

            # Return a HTTP response with the newly updated item
            return Response(read_serializer.data, status=200)

    # If the update data is not valid, return an error response
        return Response(update_serializer.errors, status=400)

class RediscoverView(APIView,
                    UpdateModelMixin,
                    DestroyModelMixin,CustomPagination):
    def get(self, request,keyid=None):
        # keyid=request.query_params.get('keyid', None)
        if keyid:
            try:
                queryset = Recom.objects.get(keyid=keyid)

            except Recom.DoesNotExist:

                return Response({'errors': 'item does not exist.'}, status=400)

            read_serializer = RecomSerializer(queryset)

            return Response(read_serializer.data)
            # Trigger update
        urlData = "http://recengineservice:8002/trigger_rediscover_updates/?method=updateStatus"
        # urlData = urlData + parse.quote(docid)
        webURL = urllib.request.urlopen(urlData)
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        resp = json.loads(data.decode(encoding))
        print("from recom update ",resp)
        datetime.date(datetime.today())
        queryset = Recom.objects.filter(displaying_date=datetime.date(datetime.today())).order_by('-score')
        queryset = self.paginate_queryset(queryset, request, view=self)
        read_serializer = RecomSerializer(queryset, many=True)
        # Return a HTTP response object with the list
        return self.get_paginated_response(read_serializer.data)

    def put(self, request,keyid=None):
        # keyid=request.query_params.get('keyid', None)
        try:
            # Check if the  item exists
            rec_item = Recom.objects.get(keyid=keyid)
        except Recom.DoesNotExist:
            # return an error response
            return Response({'errors': 'item does not exist.'}, status=400)

        # use the serializer to validate the updated data
        update_serializer = RecomSerializer(rec_item, data=request.data)

        # proceed to saving data to the database
        if update_serializer.is_valid():

            # update the item in the database
            recom_item_object = update_serializer.save()

            # Serialize the item from Python object to JSON format
            read_serializer = RecomSerializer(recom_item_object)

            urlData = "http://recengineservice:8002/trigger_rediscover_updates/?method=sm2likeCalc&keyid="+keyid
            # urlData = urlData + parse.quote(docid)
            webURL = urllib.request.urlopen(urlData)
            data = webURL.read()
            encoding = webURL.info().get_content_charset('utf-8')
            resp = json.loads(data.decode(encoding))
            print("from recom update ",resp)

            # Return a HTTP response with the newly updated item
            return Response(read_serializer.data, status=200)

        # If the update data is not valid, return an error response
        return Response(update_serializer.errors, status=400)
