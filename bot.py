import requests
import datetime
import pytz

from time import sleep # функция для создания паузы в выполнении программы

import misc #импортируем модуль с токеном бота
import talk2telegramapi # модуль с функциями общения с API Telegram
import fiitinfo  # Модуль с информацией по группе Фиит

# Задаём часовой пояс
servertz = pytz.timezon("Europe/Moscow")



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

# Функция команды schedule_init
def do_schedule_init():


# Функция команды schedule_stop
def do_schedule_stop():



# Функция команды init_up
def do_init_up():
    updown = 'up'
    # необходима авторизация изменения верх. ниж. недели


# Функция команды init_down
def do_init_down():
    updown = 'down'
    # необходима авторизация изменения верх. ниж. недели


# Функция команды

# Функция команды

# Функция команды

# Функция команды


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
    '/gruop_list':"Спсиок группы с контактами",
    '/gruop_list@FiitRndBot': "Спиcок группы с контактами"
    # Инизиализация  рассылки расписания
    '/schedule_init':
    '/schedule_init@FiitRndBot':
    # Остановка рассылки расписания
    '/schedule_stop':
    '/schedule_stop@FiitRndBot':
    # Инициализация верхней недели
    '/init_up':
    '/init_up@FiitRndBot':
    # Инициализация нижней недели
    '/init_down':
    '/init_down@FiitRndBot':

}



# Основная функция содержащая тело бота
def main():

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


        # Получаем последнее сообщенеие
        message = talk2telegramapi.get_last_message()
        msg_text = message['text']
        msg_chat_id = message['chat_id']

        # Если список сообщений не пуст тогда делаем всё что в этом if (разбор команды и ответ)
        if message:
            if last_upd_id == message['update_id']: #если оно то же самое то переходим к следующей итерации
                sleep(2)
                continue
            else:# Если нет, то обновляем значение последнего update_id и выполняем последующие команды
                last_upd_id = message['update_id']


            # Переписываем выбор команды

            if msg_text in dict_of_commands :
                # Инизиализация и остановка рассылки расписания
                if (msg_text == '/schedule_init' or msg_text == '/schedule_init@FiitRndBot'):
                    do_schedule_init(msg_chat_id)

                elif (msg_text == '/schedule_stop' or msg_text == '/schedule_stop@FiitRndBot'):
                    do_schedule_stop(msg_chat_id)

                # Инизиализация типа недели
                elif (msg_text == '/init_up' or msg_text == '/init_up@FiitRndBot'):
                    do_init_up()

                elif (msg_text == '/init_down' or msg_text == '/init_down@FiitRndBot'):
                    do_init_down()

                #  Отправляем информацию о Деканате
                elif (msg_text == '/dean'  or msg_text =='/dean@FiitRndBot'):
                    dict_of_commands[msg_text]()

                # Отправляем информацию о Дисциплинах
                elif (msg_text == '/disciplines' or msg_text == '/disciplines@FiitRndBot'):
                    dict_of_commands[msg_text]()

                # Отправляем информацию о Сессии
                elif (msg_text == '/session' or msg_text == '/session@FiitRndBot'):
                    dict_of_commands[msg_text]()

                # Отправляем список группы
                elif (msg_text == '/gruop_list' or msg_text == '/gruop_list@FiitRndBot'):
                    dict_of_commands[msg_text]()







                elif

            else:
                send_text = 'Не в списке инфо команд'
                talk2telegramapi.send_message(message['chat_id'],send_text)



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

        # print(schedule_chat_list)
        # print(now.hour)

        # Ждём 1 секунду до следующего запроса
        sleep(1)





if __name__ == '__main__':
    main()
