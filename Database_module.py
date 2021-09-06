""" Для работы модуля необходимо создать в PostgreSQL базу данных с параметрами указанными в 7-ой строке,
а также запустить данный файл для создания нужных таблиц.

"""

import sqlalchemy

dsn = 'postgresql://VK_bot:12345@localhost:5432/VKinder'   # Вход в базу "VKinder", пользователь "VK_bot", пароль "12345"
engine = sqlalchemy.create_engine(dsn)

connection = engine.connect()

x = sqlalchemy.inspect(engine).get_table_names()

if len(x) == 0:     # Команды для создания таблиц в базе
    connection.execute("""CREATE TABLE IF NOT EXISTS BotUser (
        Id SERIAL PRIMARY KEY,
        VK_id INTEGER NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS Сandidate (
        Id SERIAL PRIMARY KEY,
        VK_id INTEGER NOT NULL UNIQUE,
        Name TEXT NOT NULL,
        Reference TEXT NOT NULL,
        BotUserId INTEGER NOT NULL REFERENCES BotUser(VK_Id)
    );

    CREATE TABLE IF NOT EXISTS Photo (
        Id SERIAL PRIMARY KEY,
        ReferencePhoto TEXT NOT NULL,
        СandidateId INTEGER NOT NULL REFERENCES Сandidate(VK_id)
    );""")


class DatabaseVKinder:  # Класс для добавления данных найденных пользователь в базу

    def add_botuser(self, ids):     # Функция добавляет в базу id ищущего
        quantity = connection.execute(f"SELECT * FROM BotUser WHERE VK_id = {ids};").fetchall()
        if len(quantity) == 0:
            connection.execute(f"INSERT INTO BotUser(VK_id) VALUES({ids});")

    def add_candidate(self, vk_id, name, reference, botuser_id):    # Функция добавляет в базу данные найденого кандидата
        connection.execute(f"INSERT INTO Сandidate(VK_id, Name, Reference, BotUserId) "
                           f"VALUES({vk_id}, '{name}', '{reference}', {botuser_id});")

    def add_photo(self, list_photo, candidateId):   # Функция добавляет в базу ссылки на фото найденого кандидата
        for i in list_photo:
            connection.execute(f"INSERT INTO Photo(ReferencePhoto, СandidateId) "
                               f"VALUES('{i}', {candidateId});")

    def database_move(self, ids, lst):  # Функция принимает данные для записи и запускает внутренние функции класса
        quantity = connection.execute(f"SELECT * FROM Сandidate WHERE VK_id = {lst[1]};").fetchall()
        if len(quantity) == 0:  # Условие проверки на повторяющихся кандидатов
            self.add_botuser(ids)
            self.add_candidate(lst[1], lst[0], lst[2], ids)
            self.add_photo(lst[3], lst[1])
            print(f"Данные пользователя id {lst[1]} добавлены в базу")
        elif len(quantity) != 0:
            print("Повтор")
            return False


# for i in x: # Команда на удаление всех таблиц в базе
#     connection.execute(f"drop table {i} CASCADE")
# print(x)

