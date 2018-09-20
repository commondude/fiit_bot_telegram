import requests
import misc #импортируем модуль с токеном бота
import datetime

from time import sleep # функция для создания паузы в выполнении программы

# Определяем переменные с URL бота в API Telegram
token = misc.token
bot_url = 'https://api.telegram.org/bot'+token+'/'

# Функция: Получаем список обновлений, возвращаем словарь
def get_updates():
    url = bot_url + 'getupdates'
    r = requests.get(url)
    return r.json()

# Функция:Получаем последнее сообщение из списка обновлений, возвращаем словарём
# или False если список сообщений пуст
def get_last_message():
    data = get_updates()
    if data['result']:
        update_id = data['result'][-1]['update_id']
        chat_id = data['result'][-1]['message']['chat']['id']
        text_message = data['result'][-1]['message']['text']
        message = {'update_id':update_id, 'chat_id':chat_id,'text':text_message}
    else:
        message= False
    return message


# Функция:Отправляем текстовое сообщение в чат по указанному id
def send_message(chat_id,text='Wait...'):
    url = bot_url+'sendmessage?chat_id={}&text={}'.format(chat_id,text)
    requests.get(url)
    print(url)



# Основная функция содержащая тело бота
def main():
    # Задаём словарь информационных команд
    dict_of_info_command = {
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
    }




    # Расписание на верхнюю и на нижнюю неделю
    schedule_up = {
        0:['Непрерывная математика','Непрерывная математика'],
        1:['Основы программирования(практикум)','Основы программирования(практикум)'],
        2:['Самостоятельная работа','Самостоятельная работа'],
        3:['Основы программирования','Язык программирования C++'],
        4:['Математическая логика','Философия'],
        }
    schedule_down = {
        0:['Непрерывная математика','Философия'],
        1:['Иностранный язык','Иностранный язык'],
        2:['Самостоятельная работа','Самостоятельная работа'],
        3:['Основы программирования','Язык программирования C++'],
        4:['Основы программирования','Проект'],
        }

    # Инициализирую перемнную верхняя\нижняя неделя
    updown = 'up'
    # Инициализируем список чатов для отправки расписания
    schedule_chat_list = []
    # Флаг рассылки расписание(было сегодня разослано или нет)
    send_schedule_bool = False
    schedule = schedule_up
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
                schedule = schedule_down
                init_week = True
            elif updown=='down':
                updown = 'up'
                schedule = schedule_up
                init_week = True

        # В конце недели меням значения флага инизиализации недели
        if datetime.datetime.today().weekday() == 6 and datetime.datetime.today().hour ==23 and datetime.datetime.today().minute ==59 and datetime.datetime.today().second >= 55 :
            init_week = False


        # Получаем последнее сообщенеие
        message = get_last_message()
        # Если список сообщений не пуст тогда делаем всё что в этом if (разбор команды и ответ)
        if message:
            if last_upd_id == message['update_id']: #если оно то же самое то переходим к следующей итерации
                sleep(2)
                continue
            else:# Если нет, то обновляем значение последнего update_id и выполняем последующие команды
                last_upd_id = message['update_id']



            # Инициализируем переменную отправляемого текста
            send_text = 'foobar'
            try:#Пытаемся записать в переменную отправляемого текста значение соответствующее команде(если этот текст команда)
                send_text = dict_of_info_command[message['text']]
            except:# Если ключ в словаре не найден, значит это не инфо команда
                if (message['text'] == '/schedule_init' or message['text'] == '/schedule_init@FiitRndBot') \
                        and message['chat_id'] not in schedule_chat_list:
                    schedule_chat_list.append(message['chat_id'])
                    send_message(message['chat_id'], 'Неделя =' + updown)
                    send_message(message['chat_id'],','.join(schedule[datetime.datetime.today().weekday()]))
                elif (message['text'] == '/schedule_stop' or message['text'] == '/schedule_stop@FiitRndBot') \
                        and message['chat_id']  in schedule_chat_list:
                    schedule_chat_list.remove(message['chat_id'])
                    send_message(message['chat_id'],'Отправка расписания остановлена')
                elif message['text'] == '/init_up' or message['text'] == '/init_up@FiitRndBot':
                    updown = 'up'
                    schedule = schedule_up
                    send_message(message['chat_id'], 'Эта неделя верхняя')
                elif message['text'] == '/init_down' or message['text'] == '/init_down@FiitRndBot':
                    updown = 'down'
                    schedule = schedule_down
                    send_message(message['chat_id'], 'Эта неделя нижняя')
                else:
                    send_text = 'Не в списке инфо команд'

            # Если отправляемый текст отличен от заглушки "foobar" значит в send_text ответ на инфо команду
            if send_text != 'foobar':
                send_message(message['chat_id'],send_text)# Отправляем его в ответ на пришедшее сообщение
                print('send text= '+ send_text)
            # Если текст сообщения stop останавливаем бота
            if message['text'] == 'stop':
                print(message['text'])
                break






        # Рассылаем расписание в чаты в 9.00 если оно уже не разослано
        if datetime.datetime.today().weekday() in range(5) and datetime.datetime.today().hour == 9 and not send_schedule_bool:
            for i in schedule_chat_list:
                send_message(i, 'Неделя ='+updown)
                send_message(i, ','.join(schedule[datetime.datetime.today().weekday()]))
            send_schedule_bool = True



        # В 23 часу сбрасываем флаг отправки расписания
        if datetime.datetime.today().weekday() in range(5) and datetime.datetime.today().hour == 23 and send_schedule_bool:
            send_schedule_bool = False

        # print(schedule_chat_list)
        # print(datetime.datetime.today().hour)

        # Ждём 1 секунду до следующего запроса
        sleep(1)





if __name__ == '__main__':
    main()
