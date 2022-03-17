import datetime
import json
import threading
import time

import requests
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver


class Spam(models.Model):
    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылка"

    id = models.AutoField(primary_key=True, verbose_name="id Рассылки")
    content = models.TextField(verbose_name='Текст сообщения отправки')
    filter = models.TextField('Фильтр свойств клиентов (код оператора, тэг)')
    started_at = models.DateTimeField(verbose_name='Дата и время запуска рассылки')
    ended_at = models.DateTimeField(verbose_name='Дата и время окончания рассылки')


class Client(models.Model):
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    id = models.AutoField(primary_key=True, verbose_name='id Клиента')
    phone_number = models.CharField(validators=[RegexValidator(regex="^(7+([0-9]){10})$",
                                    message="Набран неверный формат номера телефона, введите в формате: 7XXXXXXXXXX (X - цифра от 0 до 9)")],
                                    max_length=11,
                                    verbose_name='Номер телефона')
    code = models.CharField(max_length=3, verbose_name='Код мобильного оператора')
    tag = models.CharField(max_length=100, verbose_name='Тэг (произвольная метка)')
    UTC = models.CharField(verbose_name='Часовой пояс', max_length=10)


class Message(models.Model):
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    id = models.AutoField(primary_key=True, verbose_name='id Сообщения')
    status = models.CharField(max_length=20, verbose_name='Статус отправки')
    spam_id = models.IntegerField()
    client_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания сообщения')


def spam_to_users(spam_info):
    tag_or_code = spam_info.filter.split(', ')
    clients = Client.objects.filter(Q(code=tag_or_code[0])
                                    and Q(tag=tag_or_code[1]))

    for client in clients:
        Message(status="Ожидает отправки", spam_id=spam_info.id, client_id=client.id).save()

    current_date = datetime.datetime.now()

    while (spam_info.ended_at.replace(tzinfo=None) - current_date) > datetime.timedelta(seconds=1):

        if (spam_info.started_at.replace(tzinfo=None) - current_date) <= datetime.timedelta(seconds=1):
            messages = Message.objects.filter(Q(status="Ожидает отправки") or Q(status="Ошибка отправки"))

            if messages:
                for message in messages:
                    message_text = spam_info.content
                    client_instance = Client.objects.get(id=message.client_id)
                    message_phone = client_instance.phone_number

                    url = f'https://probe.fbrq.cloud/v1/send/{message.id}'

                    headers = {
                        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Nzg5NTMwNTQsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IkxJR1VTS0tBRGV2In0.2xAEkv5uEBHaMkTcdY2ALg0R_vCjK7Crynhglk1naE8',
                    }

                    body = {
                        'id': int(message.id),
                        'phone': int(message_phone),
                        'text': message_text,
                    }
                    json_body = json.dumps(body)

                    print("Выполняем запрос")

                    res = requests.post(url, headers=headers, data=json_body, timeout=5)

                    if res.status_code == 200:
                        message.status = "Отправлено"
                        message.save()
                    else:
                        message.status = "Ошибка отправки"
                        message.save()

                    current_date = datetime.datetime.now()

            else:
                break

        else:
            print("Ждём нужного времени")
            time.sleep(10)
            current_date = datetime.datetime.now()


@receiver(post_save, sender=Spam)
def create_folder(sender, instance, created, **kwargs):
    if created:
        spam = threading.Thread(target=spam_to_users, args=(instance,))
        spam.start()
