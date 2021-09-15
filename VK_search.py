import requests
from random import randrange
import datetime


class VKcandidat:   # Класс для поиска в ВК подходящих кандидатов по данным запрашиваемого (возраст, пол, город, семейное положение)
    url = "https://api.vk.com/method/"
    version = 5.131
    users_params = {}
    user_age = int

    def __init__(self, token):
        self.token = token

    def users_get(self):  # Функция получает информацио о пользователе по его токену
        params = {"access_token": self.token,
                  "v": self.version,
                  "fields": "sex, bdate, city, relation"
                  }
        requests_test = requests.get(self.url + "users.get", params).json()
        self.users_params = requests_test

    def age(self):      # Функция для вычисления возраста запрашиваемого (в выдаче api ВК есть только дата рождения)
        date_now = datetime.datetime.now()
        birthday = self.users_params['response'][0]['bdate']
        x = datetime.datetime.strptime(birthday, '%d.%m.%Y')
        s = str(date_now - x)
        ans = int(s[:s.find(" ")]) // 365
        self.user_age = ans

    def upload_search(self):    # Функция поиска подходящих кандидатов по данным запрашиваемого
        params = {"access_token": self.token,
                  "v": self.version,
                  "count": 999,
                  "fields": "sex, bdate, city, relation",
                  "age_from": self.user_age,
                  "age_to": self.user_age,
                  "sex": -(self.users_params['response'][0]['sex']) + 3,
                  "status": 6,
                  "city": self.users_params['response'][0]['city']['id']
                  }
        requests_test = requests.get(self.url + "users.search", params).json()  # Получение от ВК json-ответа
        return requests_test

    def upload_foto(self, ids):     # Функция возващает топ 3 (или меньше) фотографии по id пользователя
        params = {"access_token": self.token,
                  "v": self.version,
                  "user_id": ids,
                  "album_id": 'profile',
                  "extended": 1
                  }
        requests_test = requests.get(self.url + "photos.get", params).json()
        if 'error' in requests_test or requests_test['response']['count'] == 0:
            return False
        else:
            dict_foto = {}      # В этот словарь добавляются ссылки на фото
            for i in requests_test['response']['items']:
                dict_foto[i["likes"]["count"]] = i['id']
            sor = sorted(list(dict_foto.keys()))
            if len(sor) >= 3:
                return [dict_foto[sor[-1]], dict_foto[sor[-2]], dict_foto[sor[-3]]]
            elif len(sor) == 2:
                return [dict_foto[sor[-1]], dict_foto[sor[-2]]]
            else:
                return [dict_foto[sor[-1]]]

    def sorting(self):  # Фукция объединяет в один список данные и фото всех подходящих кандидатов
        self.users_get()    # Единоразовый запуск функции для получения и записи данных пользователя чата
        self.age()
        response = self.upload_search()
        lst = []
        for data in response['response']['items']:
            if data['can_access_closed'] and data['is_closed'] is False:
                lst.append([f"{data['first_name']} {data['last_name']}"])
                lst[-1].append(data['id'])
                lst[-1].append(f"https://vk.com/id{data['id']}")
        return lst

    def random_candidate(self):  # Функция возвращает случайного кандидата с фотками из множества подходящих
        users = self.sorting()
        candidate = users[randrange(len(users))]
        candidate.append(self.upload_foto(candidate[1]))
        return candidate
