#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render

import models
from django.http import Http404,HttpResponse
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny
import serializers
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from uuid import UUID
from .forms import *
from users.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse_lazy
from django_vanilla.django_vanilla import ListView, CreateView, DetailView, UpdateView, DeleteView
from dateutil.parser import *
from decimal import Decimal
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions  import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class ItemEndpoint(APIView):

    def post(self, request):
        serializer =  serializers.ItemSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            image_obj = request.FILES.get("picture")
            user,_ = User.objects.get_or_create(mobile=data["mobile"])
            item,created = models.Item.objects.get_or_create(name=data["name"],created=parse(data["created"]))
            if data.get("picture"):
                item.image = data["picture"]
                item.save()
            entry = models.Entry.objects.create(item=item,user=user,type="inventory",amount=Decimal(data["total_cost"]),quantity=int(data["quantity"]))


            return Response(serializers.ItemSerializer(item).data, status=status.HTTP_201_CREATED)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
    
        items = models.Item.objects.all()
        mobile = self.request.GET.get("mobile")

        if mobile:
            items = items.filter(user__mobile=mobile)
           
        serializer = serializers.ItemSerializer(items, many=True,context={'request':request})
        return Response(serializer.data)

class EntryEndpoint(APIView):

    def post(self, request):
       
        serializer =  serializers.EntrySerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            user,_ = User.objects.get_or_create(mobile=data["mobile"])
            item,_ = models.Item.objects.get_or_create(name=data["name"])
            entry = models.Entry.objects.create(item=item,user=user,type=data["type"],amount=Decimal(data["amount"]),quantity=int(data["quantity"]),created=parse(data["created"]),customer_mobile=data["customer_mobile"],transaction_type=data["transaction_type"])

            return Response(serializers.EntrySerializer(entry).data, status=status.HTTP_201_CREATED)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
      
        entries = models.Entry.objects.all()
        mobile = self.request.GET.get("mobile")

        if mobile:
            entries = entries.filter(user__mobile="mobile")
           
        serializer = serializers.EntrySerializer(entries, many=True,context={'request':request})
        return Response(serializer.data)



class NotificationList(ListView):
    model = Notification
    paginate_by = 20


class NotificationCreate(CreateView):
    model = Notification
    form_class = NotificationForm
    success_url = reverse_lazy('bookkeeping:notification-list')


class NotificationDetail(DetailView):
    model = Notification


class NotificationUpdate(UpdateView):
    model = Notification
    form_class = NotificationForm
    success_url = reverse_lazy('bookkeeping:notification-list')


class NotificationDelete(DeleteView):
    model = Notification
    success_url = reverse_lazy('bookkeeping:notification-list')

class ChangePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = serializers.ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, 
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            update_session_auth_hash(request, self.object)
            return Response({"status":"success"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    accountType = request.data.get("accountType")
    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    if user.first_login == True:
        first_login = False
        user.first_login=True
        user.save()
    else:
        first_login=True
    return Response({"token": token.key,"first_login":first_login})

@api_view(["POST"])
def createAccount(request):
    username = request.data.get("username")
    password = request.data.get("password")
    idd = request.data.get("id")
    accountType = request.data.get("accountType")
    if not username:
        return Response({"message": "username is required"},status=status.HTTP_400_BAD_REQUEST)

    if not id:
        return Response({"message": "id is required"},status=status.HTTP_400_BAD_REQUEST)
    if not password:
        return Response({"message": "password is required"},status=status.HTTP_400_BAD_REQUEST)


   
    try:
        user = User.objects.create(
                username = username,
                account_type=accountType,

        )

        cbo = models.Cbo.objects.get(id=int(idd))

        user.set_password(request.data.get("password"))
        user.save()
        cbo.users.add(user)
    except Exception as e:
        return Response({"message": str(e)},status=status.HTTP_400_BAD_REQUEST)

    return Response({"status": "success"})


class TagEndpoint(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        """
        Return a list of tags
        """
        tags = Post.tags.tag_model.objects.all().distinct()
        
        serializer = TagsSerializer(tags, many=True,context={'request':request})
        return Response(serializer.data)

class CBOEndpoint(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return models.Cbo.objects.get(pk=pk)
        except models.Cbo.DoesNotExist:
            raise Http404

    def post(self, request):
       
        serializer =  serializers.CBOSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
      
        cbos = models.Cbo.objects.all()
       
           
        serializer = serializers.CBOSerializer(cbos, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        
        cbo  = self.get_object(pk)

        old = serializers.CBOSerializer(cbo).data.copy()
        old.update(request.data)

        serializer = serializers.CBOSerializer(cbo, data=old)
        if serializer.is_valid():
            cbo = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnventureEndpoint(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return models.Enventure.objects.get(pk=pk)
        except models.Enventure.DoesNotExist:
            raise Http404

    def post(self, request):
       
        serializer =  serializers.EnventureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
      
        enventures = models.Enventure.objects.all()  
        serializer = serializers.EnventureSerializer(enventures, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        
        enventure  = self.get_object(pk)

        old = serializers.EnventureSerializer(enventure).data.copy()
        old.update(request.data)

        serializer = serializers.EnventureSerializer(enventure, data=old)
        if serializer.is_valid():
            enventure = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountsEndpoint(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def post(self, request):
       
        serializer =  serializers.CBOSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            user,_ = User.objects.get_or_create(mobile=data["mobile"])
            item,_ = models.Item.objects.get_or_create(name=data["name"])
            entry = models.Entry.objects.create(item=item,user=user,type=data["type"],amount=Decimal(data["amount"]),quantity=int(data["quantity"]),created=parse(data["created"]),customer_mobile=data["customer_mobile"],transaction_type=data["transaction_type"])

            return Response(serializers.CBOSerializer(entry).data, status=status.HTTP_201_CREATED)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
      
        entries = models.Entry.objects.all()
        mobile = self.request.GET.get("mobile")

        if mobile:
            entries = entries.filter(user__mobile="mobile")
           
        serializer = serializers.EntrySerializer(entries, many=True,context={'request':request})
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Delete a post
        ``````````````````````
        :pparam integer id: the id of the post
        """
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        """
        Update an post
        ``````````````````````

        Update various attributes and configurable settings for the given
       post

        :pparam number id: id of the post

        """

       
        post  = self.get_object(pk)

        
        
        old = PostSerializer(post).data.copy()
        old.pop("image")
        old.update(request.data)

        serializer = PostSerializer(post, data=old,context={'request': request})
        if serializer.is_valid():
            post = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CBODataEndpoint(APIView):
   
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404


    def get(self, request):
      
        entries = models.Entry.objects.all()
        mobile = self.request.GET.get("pk")
           
        serializer = serializers.EntrySerializer(entries, many=True,context={'request':request})
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Delete a post
        ``````````````````````
        :pparam integer id: the id of the post
        """
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CBODetailEndpoint(APIView):
    permission_classes = (IsAuthenticated,)



    def get(self, request):
        user=request.user
        cbo =user.cbo
    
        serializer = serializers.CBOSerializer(cbo)
        return Response(serializer.data)

class EnventureDetailEndpoint(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user=request.user
        enventure =user.enventure
        serializer = serializers.EnventureSerializer(enventure,context={'request':request})
        return Response(serializer.data)





