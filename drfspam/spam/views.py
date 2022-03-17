from rest_framework import viewsets, mixins
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
