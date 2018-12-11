import requests
import misc #импортируем модуль с токеном бота

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
    try:
        if data['result']:
            update_id = data['result'][-1]['update_id']
            chat_id = data['result'][-1]['message']['chat']['id']
            text_message = data['result'][-1]['message']['text']
            message = {'update_id':update_id, 'chat_id':chat_id,'text':text_message}
        else:
            for i in data:
                print(i,data[i])
            message = False
    except:
        message= False
        print('Нет новых сообщений.')
        print(type(data))
        print(data.keys())
        print(data.values())
    return message

# Функция:Отправляем текстовое сообщение в чат по указанному id
def send_message(chat_id,text='Wait...'):
    url = bot_url+'sendmessage?chat_id={}&text={}'.format(chat_id,text)
    requests.get(url)
