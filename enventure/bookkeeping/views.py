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


class ItemEndpoint(APIView):

    def post(self, request):
        serializer =  serializers.ItemSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            user,_ = User.objects.get_or_create(mobile=data["mobile"])
            item,created = models.Item.objects.get_or_create(name=data["name"],created=parse(data["created"]))
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


class TagEndpoint(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        """
        Return a list of tags
        """
        tags = Post.tags.tag_model.objects.all().distinct()
        
        serializer = TagsSerializer(tags, many=True,context={'request':request})
        return Response(serializer.data)



