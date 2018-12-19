import requests
import datetime
import pytz
import jokeAndWeather

from time import sleep # функция для создания паузы в выполнении программы
import talk2telegramapi # модуль с функциями общения с API Telegram
import fiitinfo  # Модуль с информацией по группе Фиит



# Функция команды schedule_init
def do_schedule_init(chat_id,schedule_chat_list):
    if chat_id not in schedule_chat_list:
        schedule_chat_list.append(chat_id)
        talk2telegramapi.send_message(chat_id,'Ваш чат добавлен в список рассылки.')
    else:
        talk2telegramapi.send_message(chat_id,'Ваш чат уже есть в списке рассылки.')



# Функция команды schedule_stop
def do_schedule_stop(chat_id,schedule_chat_list):
    if chat_id  in schedule_chat_list:
        schedule_chat_list.remove(chat_id)
        talk2telegramapi.send_message(chat_id,'Ваш чат удалён из списка рассылки.')
    else:
        talk2telegramapi.send_message(chat_id,'Вашего чата нет в списке рассылки.')



# Функция команды init_up
def do_init_up(chat_id):
    talk2telegramapi.send_message(chat_id,'Теперь неделя верхняя.')
    return fiitinfo.schedule_up, 'up'
    # необходима авторизация изменения верх. ниж. недели


# Функция команды init_down
def do_init_down(chat_id):
    talk2telegramapi.send_message(chat_id,'Теперь неделя нижняя.')
    return fiitinfo.schedule_down, 'down'
    # необходима авторизация изменения верх. ниж. недели



# Задаём словарь информационных команд
dict_of_commands = {
    # Информация о деканате
    '/dean':'Информация о деканате',
    '/dean@FiitRndBot':'Информация о деканате',
    # Информация о дисциплинах
    '/disciplines':'Информация о дисциплинах',
    '/disciplines@FiitRndBot':'Информация о дисциплинах',
    # Информация о сессии
    '/session':'Информация о сессии',
    '/session@FiitRndBot':'Информация о сессии',
    # Спсиок группы с контактами
    '/group_list':"Спсиок группы с контактами",
    '/group_list@FiitRndBot': "Спиcок группы с контактами",
    # Инизиализация  рассылки расписания
    '/schedule_init':'Инизиализация рассылки расписания',
    '/schedule_init@FiitRndBot':'Инизиализация рассылки расписания',
    # Остановка рассылки расписания
    '/schedule_stop':'Остановка рассылки расписания',
    '/schedule_stop@FiitRndBot':'Остановка рассылки расписания',
    # Инициализация верхней недели
    '/init_up':'Инициализация верхней недели',
    '/init_up@FiitRndBot':'Инициализация верхней недели',
    # Инициализация нижней недели
    '/init_down':'Инициализация нижней недели',
    '/init_down@FiitRndBot':'Инициализация нижней недели',
    # Расписание на неделю
    '/schedule_week':'Расписание на эту неделю',
    '/schedule_week@FiitRndBot':'Расписание на эту неделю',
    # Службная команда
    '/vars':'Значения переменных в стандартный вывод',
    '/vars@FiitRndBot':'Значения переменных в стандартный вывод',
    # Погода в Ростове
    '/weather':'Прогноз погоды',
    '/weather@FiitRndBot':'Прогноз погоды',
    # Анекдот
    '/joke':'Анекдот',
    '/joke@FiitRndBot':'Анекдот'
}




# Основная функция содержащая тело бота
def main():
    # Задаём часовой пояс
    servertz = pytz.timezone("Europe/Moscow")

    # То что нужно считывать и записывать на диск.
    # Инициализирую перемнную верхняя\нижняя неделя
    updown = 'up'
    # Инициализируем список чатов для отправки расписания
    schedule_chat_list = []
    # Флаг рассылки расписание(было сегодня разослано или нет)
    send_schedule_bool = False
    schedule = fiitinfo.schedule_up
    # Задаём значение последнего update_id
    last_upd_id = 1
    # Флаг инициализации недели
    init_week = False



    # Бесконечный цикл бота
    while True:
        #  Меняем значение верхней нижней недели
        if not init_week:
            if updown=='up':
                updown = 'down'
                schedule = fiitinfo.schedule_down
                init_week = True
            elif updown=='down':
                updown = 'up'
                schedule = fiitinfo.schedule_up
                init_week = True

        # Переманная текущего дня и времени по Москве
        now = datetime.datetime.now(servertz)

        # В конце недели меням значения флага инизиализации недели
        if now.weekday() == 6 and now.hour ==23 and now.minute ==59 and now.second >= 55 :
            init_week = False
            sleep(10)#Избегаем повторноо переключения недели. Изменение этой перевнной должно быть 1 раз в неделю


        # Получаем последнее сообщенеие
        message = talk2telegramapi.get_last_message()


        # Если список сообщений не пуст тогда делаем всё что в этом if (разбор команды и ответ)
        if message:
            if last_upd_id == message['update_id']: #если оно то же самое то переходим к следующей итерации
                sleep(2)
                continue
            else:# Если нет, то обновляем значение последнего update_id и выполняем последующие команды
                last_upd_id = message['update_id']

            # Присваиваем переменным значения из вновь пришедшего сообщения
            msg_text = message['text']
            msg_chat_id = message['chat_id']

            # Переписываем выбор команды

            if msg_text in dict_of_commands :
                # Инизиализация и остановка рассылки расписания
                if (msg_text == '/schedule_init' or msg_text == '/schedule_init@FiitRndBot'):
                    do_schedule_init(msg_chat_id,schedule_chat_list)

                elif (msg_text == '/schedule_stop' or msg_text == '/schedule_stop@FiitRndBot'):
                    do_schedule_stop(msg_chat_id,schedule_chat_list)

                # Инизиализация типа недели
                elif (msg_text == '/init_up' or msg_text == '/init_up@FiitRndBot'):
                    schedule, updown = do_init_up(msg_chat_id)

                elif (msg_text == '/init_down' or msg_text == '/init_down@FiitRndBot'):
                    schedule, updown = do_init_down(msg_chat_id)

                #  Отправляем информацию о Деканате
                elif (msg_text == '/dean'  or msg_text =='/dean@FiitRndBot'):
                    talk2telegramapi.send_message(msg_chat_id,fiitinfo.dean_info)

                # Отправляем информацию о Дисциплинах
                elif (msg_text == '/disciplines' or msg_text == '/disciplines@FiitRndBot'):
                    disciplines = ''
                    for i in fiitinfo.disciplines:
                        disciplines += i['name']+'\n'+i['teacher']+'\n'+i['phone']+'\n'+'\n'
                    talk2telegramapi.send_message(msg_chat_id,disciplines)

                # Отправляем информацию о Сессии
                elif (msg_text == '/session' or msg_text == '/session@FiitRndBot'):
                    talk2telegramapi.send_message(msg_chat_id,fiitinfo.session_info)

                # Отправляем список группы
                elif (msg_text == '/group_list' or msg_text == '/group_list@FiitRndBot'):
                    grouplist = ''
                    for i in fiitinfo.students:
                        grouplist += i['firstname']+' '+i['surname']+' '+i['patronymic']+' '+'\n'+i['phone']+'\n'+'Номер в журнале'+i['journal_number']+'\n'+'\n'

                    talk2telegramapi.send_message(msg_chat_id,grouplist)

                elif (msg_text == '/schedule_week' or msg_text == '/schedule_week@FiitRndBot'):
                    schedule_week = ''
                    for i in range(0,5):
                        schedule_week += fiitinfo.week_days[i]+'\n'+ str(schedule[i]) +'\n'+'\n'
                    talk2telegramapi.send_message(msg_chat_id,schedule_week)

                elif (msg_text == '/vars' or msg_text == '/vars@FiitRndBot'):
                    print('schedule_chat_list= ',schedule_chat_list)
                    print('updown= ',updown)
                    print('send_schedule_bool= ',send_schedule_bool)
                    print('schedule= ',schedule)
                    print('Время на сервере ',now)

                # Тут команда с погодой
                elif (msg_text == '/weather' or msg_text == '/weather@FiitRndBot'):
                    talk2telegramapi.send_message(msg_chat_id,jokeAndWeather.weather_from_darksky())

                # а тут и анекдот подъедет
                elif (msg_text == '/joke' or msg_text == '/joke@FiitRndBot'):
                    talk2telegramapi.send_message(msg_chat_id,jokeAndWeather.joke())

                else:
                    talk2telegramapi.send_message(msg_chat_id,'Кто-то забыл прописать функцию для команды.')

            else:
                talk2telegramapi.send_message(message['chat_id'],'Не в списке команд')



            # Если текст сообщения stop останавливаем бота
            if msg_text == 'stop':
                talk2telegramapi.send_message(message['chat_id'],"Oh No!... I'am dying...",)
                break






        # Рассылаем расписание в чаты в 9.00 если оно уже не разослано
        if now.weekday() in range(5) and now.hour == 9 and not send_schedule_bool:
            for i in schedule_chat_list:
                talk2telegramapi.send_message(i, 'Неделя ='+updown)
                talk2telegramapi.send_message(i, ','.join(schedule[now.weekday()]))
            send_schedule_bool = True



        # В 23 часу сбрасываем флаг отправки расписания
        if now.weekday() in range(5) and now.hour == 23 and send_schedule_bool:
            send_schedule_bool = False


        # Ждём 1 секунду до следующего запроса
        sleep(1)





if __name__ == '__main__':
    main()
