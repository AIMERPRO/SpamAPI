import json

from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Spam, Client, Message
from .serializers import ClientSerializer, SpamSerializer, MessageSerializer


# ViewSet для POST, GET, PUT, DELETE запросов по клиентам
class ClientViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer


# ViewSet для всех запросов по рассылке
class SpamViewSet(viewsets.ModelViewSet):

    queryset = Spam.objects.all()
    serializer_class = SpamSerializer


# ViewSet для GET запросов сообщений
class MessageViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer


# ViewSet для GET запросов по получению статистики сообщений по рассылкам
class SpamStatViewSet(viewsets.ViewSet):
    def list(self, request):
        spams = Spam.objects.all()
        data = []
        for spam in spams:
            messages_good = Message.objects.filter(Q(spam_id=spam.id) and Q(status="Отправлено")).count()  # Количество отправленных сообщений
            messages_wait = Message.objects.filter(Q(spam_id=spam.id) and Q(status="Ожидает отправки")).count()  # Количество сообщений ждущих отправки
            messages_bad = Message.objects.filter(Q(spam_id=spam.id) and Q(status="Ошибка отправки")).count()  # Количество сообщений с ошибками
            stat_data = {
                "id": spam.id,
                "messages_sent": messages_good,
                "messages_waiting": messages_wait,
                "messages_bad": messages_bad
            }
            data.append(stat_data)
        data = json.dumps(data)
        loaded_data = json.loads(data)
        return Response(loaded_data)
