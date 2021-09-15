""" Основной файл для запуска бота

Для корректной работы бота, на компьютере необходимо создать базу данных,
с параметрами указанными в модуле "Database_module.py"

"""

import vk_api
from random import randrange
from VK_search import VKcandidat
from Database_module import DatabaseVKinder
from vk_api.longpoll import VkLongPoll, VkEventType


token = input('Group token: ')

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message, attachment):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7), 'attachment': attachment})


if __name__ == "__main__":
    user_token = ""
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                if request == "привет" or request == "Привет":
                    write_msg(event.user_id, f"Хай. Если хочешь найти себе пару введи свой токен. =)", "")
                elif len(request) == 85:    # Условие для определения того, что пользователь ввёл свой токен.
                    user_token = request
                    can = VKcandidat(user_token)
                    x = can.random_candidate()
                    data = DatabaseVKinder()
                    data_response = data.database_move(event.user_id, x)
                    write_msg(event.user_id, f"Подходящая пара:  {str(x[0])}", "")
                    write_msg(event.user_id, f"Страница:  {str(x[2])}", "")
                    write_msg(event.user_id, f"Фотографии:", "")
                    for i in x[3]:
                        write_msg(event.user_id, "", f"photo{x[1]}_{i}")
                elif request == "найти":
                    if user_token:
                        can = VKcandidat(user_token)
                        x = can.random_candidate()
                        data = DatabaseVKinder()
                        data_response = data.database_move(event.user_id, x)
                        if data_response is False:
                            write_msg(event.user_id, f"Попробуй ещё", "")
                        else:
                            write_msg(event.user_id, f"Подходящая пара:  {str(x[0])}", "")
                            write_msg(event.user_id, f"Страница:  {str(x[2])}", "")
                            write_msg(event.user_id, f"Фотографии:", "")
                            for i in x[3]:
                                write_msg(event.user_id, "", f"photo{x[1]}_{i}")
                    else:
                        write_msg(event.user_id, f"Хай. Если хочешь найти себе пару введи свой токен. =)", "")
                else:
                    write_msg(event.user_id, "Не поняла вашего ответа...", "")
