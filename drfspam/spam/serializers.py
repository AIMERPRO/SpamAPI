from rest_framework import serializers

from .models import Spam, Client, Message


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'phone_number', 'code', 'tag', 'UTC')

    def __init__(self, *args, **kwargs):
        super(ClientSerializer, self).__init__(*args, **kwargs)

        self.fields['phone_number'].error_messages['required'] = 'Пожалуйста, введите свой номер телефона'
        self.fields['phone_number'].error_messages['invalid'] = 'Набран неверный формат номера телефона, введите в формате: 7XXXXXXXXXX (X - цифра от 0 до 9)'


class SpamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spam
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
