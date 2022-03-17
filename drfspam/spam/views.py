from django.db.models import Count
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets, mixins
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Spam, Client, Message
from .serializers import ClientSerializer, SpamSerializer, MessageSerializer


class ClientViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class SpamViewSet(viewsets.ModelViewSet):

    queryset = Spam.objects.all()
    serializer_class = SpamSerializer


class MessageViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
