import requests
import misc
import datetime

from time import sleep

token = misc.token
bot_url = 'https://api.telegram.org/bot'+token+'/'

# Получаем список обновлений, возвращаем словарь
def get_updates():
    url = bot_url + 'getupdates'
    r = requests.get(url)
    return r.json()

# Получаем последнее сообщение из списка обновлений, возвращаем словарём
def get_last_message():
    data = get_updates()
    update_id = data['result'][-1]['update_id']
    chat_id = data['result'][-1]['message']['chat']['id']
    text_message = data['result'][-1]['message']['text']
    message = {'update_id':update_id, 'chat_id':chat_id,'text':text_message}
    return message


# Отправляем текстовое сообщение в чат по указанному id
def send_message(chat_id,text='Wait...'):
    url = bot_url+'sendmessage?chat_id={}&text={}'.format(chat_id,text)
    requests.get(url)
    print(url)




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
        '/gruop_list@FiitRndBot': "Спсиок группы с контактами"
    }




    # Расписание на верхнюю и на нижнюю неделю
    schedule_up = {
        0:['Непрерывная математика','Дискретная математика'],
        1:['Иностранный язык','Иностранный язык'],
        2:['Самостоятельная работа','Самостоятельная работа'],
        3:['Алгебра и Геометрия','Алгебра и Геометрия'],
        4:['История','История'],
        }
    schedule_down = {
        0:['Непрерывная математика','Непрерывная математика'],
        1:['Дискретная математика','Дискретная математика'],
        2:['Самостоятельная работа','Самостоятельная работа'],
        3:['Алгебра и Геометрия','Алгебра и Геометрия'],
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


    # Бесконечный цикл бота
    while True:
        # В понедельник меняем значение верхней нижней недели
        if datetime.datetime.today().weekday() == 0 and updown=='up':
            updown = 'down'
            schedule = schedule_down
        elif datetime.datetime.today().weekday() == 0 and updown=='down':
            updown = 'up'
            schedule = schedule_up
        # Получаем последнее сообщенеие
        message = get_last_message()
        if last_upd_id == message['update_id']: #если оно то же самое то переходим к следующей итерации
            sleep(2)
            continue
        else:# Если нет, то обновляем значение последнего update_id
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
            elif message['text'] == '/init_down@FiitRndBot' or message['text'] == '/init_down@FiitRndBot':
                updown = 'down'
                schedule = schedule_down
                send_message(message['chat_id'], 'Эта неделя нижняя')
            else:
                send_text = 'Не в списке инфо команд'

        # Если отправляемый текст отличен от заглушки "foobar" значит в send_text ответ на инфо команду
        if send_text != 'foobar':
            send_message(message['chat_id'],send_text)# Отправляем его в ответ на пришедшее сообщение
            print('send text= '+ send_text)

        # Рассылаем расписание в чаты
        if datetime.datetime.today().weekday() in range(5) and datetime.datetime.today().hour == 19 and send_schedule_bool==False:
            for i in schedule_chat_list:
                send_message(i, 'Неделя ='+updown)
                send_message(i, ','.join(schedule[datetime.datetime.today().weekday()]))
            send_schedule_bool = True

        # В 23 часу сбрасываем флаг отправки расписания
        if datetime.datetime.today().weekday() in range(5) and datetime.datetime.today().hour == 23 and send_schedule_bool == True:
            send_schedule_bool = False

        print(schedule_chat_list)
        print(datetime.datetime.today().hour)
        # Ждём 2 секунды до следующего запроса, если текст сообщения = stop, то тогда останавливаем бота
        sleep(2)
        if message['text'] == 'stop':
            print(message['text'])
            break




if __name__ == '__main__':
    main()