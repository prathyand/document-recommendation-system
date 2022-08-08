# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from recomapiservice.serializers import User_intrSerializer
from rest_framework import status


class UserInteractionsView(APIView,
                     UpdateModelMixin,
                     DestroyModelMixin):

    def post(self, request, format=None):
        serializer = User_intrSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



