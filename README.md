# SpamAPI
Рассылка сообщений по API
## Запуск приложения
```
$ cd drfspam
```
```
$ docker-compose up --build
```

## Модели

### Модель Рассылки
![image](https://user-images.githubusercontent.com/42303843/159278705-d2fb7251-5f18-4bca-8d2c-e6f4edf405e3.png)

### Модель  Клиентов
![image](https://user-images.githubusercontent.com/42303843/159278894-f87dba40-2b3f-4397-b800-e7b849cfb7e8.png)

### Модель Сообщений
![image](https://user-images.githubusercontent.com/42303843/159279066-5c87cae3-a18f-4ba0-bc09-d4f9c6ca8889.png)

## Представления

### Представление API Клиента
![image](https://user-images.githubusercontent.com/42303843/159279414-d3f56d34-bc17-4608-b481-7bc316322a74.png)

> Запрос к этому представлению ``` /api/v1/client```

### Представление API Рассылки
![image](https://user-images.githubusercontent.com/42303843/159279850-6003badd-0f4a-4194-84a0-f47f43975876.png)

> Запрос к этому представлению ``` /api/v1/spam```

### Представление API Сообщений
![image](https://user-images.githubusercontent.com/42303843/159280007-46c2759b-f6e5-479c-81c6-6924d79d1c6b.png)

> Запрос к этому представлению ``` /api/v1/message```

### Представление API Статистики по Рассылке
![image](https://user-images.githubusercontent.com/42303843/159280309-5f5485cd-8bdc-4530-86c4-36c45e7f2140.png)

> Запрос к этому представлению ``` /api/v1/spamstatus```

## Документация к REST запросам

> Документация по всем REST запросам производится через автодокументацию с помощью drf_yasg
> Докуметация находится по адресу ```/docs/```
