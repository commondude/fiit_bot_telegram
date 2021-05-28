import datetime # библиотка для работы с датой и временем
import pytz # библиотека для работы с часовыми поясами
# import json # библиотка для работы со стандартом json
from threading import Thread # Модуль для работы с потоками
# from pickle import dumps,loads
from json import dumps,loads

import jokeAndWeather # Погода и анекдоты
from time import sleep # функция для создания паузы в выполнении программы
import talk2telegramapi # модуль с функциями общения с API Telegram
import fiitinfo  # Модуль с информацией по группе Фиит
import misc # Модуль с токеном бота
import train_verbs # Модуль с тренировкой англ глаголов


from os import environ # модуль для работы с переменными окружения для heroku
import psycopg2 # Модуль для работы с БД PostgreSQL

# Модуль с вебсервером Flask
from flask import Flask
from flask import request

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker,declarative_base

# Функция для записи данных в БД
def write_2_db(fiit_dictionary_loc):
	try:
		#sqlalchemy
		lst.updown = fiit_dictionary_loc['updown']
		lst.schedule_list = dumps(fiit_dictionary_loc['schedule_chat_list'])
		lst.last_update_id = fiit_dictionary_loc['last_upd_id']
		lst.init_week = fiit_dictionary_loc['init_week']
		lst.restart_count = fiit_dictionary_loc['restart_count']
		lst.send_schedule_bool = fiit_dictionary_loc['send_schedule_bool']
		session.commit()
		return True
		#init_week = %s, 		fiit_dictionary_loc['init_week'],
	except Exception as e:
		print(e)
		return False


# Функция команды schedule_init
def do_schedule_init(chat_id,fiit_dictionary_loc):
	if chat_id not in fiit_dictionary_loc['schedule_chat_list']:
		print(type(fiit_dictionary_loc['schedule_chat_list']))
		fiit_dictionary_loc['schedule_chat_list'].append(chat_id)
		write_2_db(fiit_dictionary_loc)
		talk2telegramapi.send_message(chat_id,'Ваш чат добавлен в список рассылки.')
	else:
		talk2telegramapi.send_message(chat_id,'Ваш чат уже есть в списке рассылки.')
	return fiit_dictionary_loc


# Функция команды schedule_stop
def do_schedule_stop(chat_id, fiit_dictionary_loc):
	if chat_id in fiit_dictionary_loc['schedule_chat_list']:
		fiit_dictionary_loc['schedule_chat_list'].remove(chat_id)
		write_2_db(fiit_dictionary_loc)
		talk2telegramapi.send_message(chat_id,'Ваш чат удалён из списка рассылки.')
	else:
		talk2telegramapi.send_message(chat_id,'Вашего чата нет в списке рассылки.')
	return fiit_dictionary_loc


# Функция команды init_up
def do_init_up(chat_id):

	fiit_dictionary['updown'] = 'up'
	write_2_db(fiit_dictionary)
	talk2telegramapi.send_message(chat_id,'Теперь неделя верхняя.')
	return fiitinfo.schedule_up
	# необходима авторизация изменения верх. ниж. недели


# Функция команды init_down
def do_init_down(chat_id):
	fiit_dictionary['updown'] = 'down'
	write_2_db(fiit_dictionary)
	talk2telegramapi.send_message(chat_id,'Теперь неделя нижняя.')
	return fiitinfo.schedule_down
	# необходима авторизация изменения верх. ниж. недели



""" Читаем в словарь из БД"""

DATABASE_URL = environ['DATABASE_URL']

"""sqlalchemy"""
connection_string = 'postgresql'+DATABASE_URL[8:]
try:
	engine = create_engine(connection_string,echo=False)
	Session = sessionmaker(bind=engine)
	talk2telegramapi.send_message('169294743','Коннект к БД успешный')
except:
	talk2telegramapi.send_message('169294743','Не могу законнектиться к БД')
	print('Не могу законнектиться к БД')

session = Session()
Base = declarative_base()

"""ORM класс таблицы состояния приложения DataBase first"""
class LastState(Base):
	__tablename__ = 'last_state'

	id = Column(Integer, primary_key=True)
	updown = Column(Text)
	schedule_list = Column(Text)
	last_update_id = Column(Text)
	init_week = Column(Boolean)
	restart_count = Column(Integer)
	send_schedule_bool = Column(Boolean)

	def __repr__(self):
		return "<LastState(updown='%s', schedule_list='%s', last_update_id='%s', init_week='%s', restart_count='%s', send_schedule_bool='%s')>"%(
				self.updown,self.schedule_list,self.last_update_id,self.init_week,self.restart_count,self.send_schedule_bool)

lst=session.query(LastState).filter(LastState.id==1).first()
fiit_dictionary = {}
fiit_dictionary.update({'updown':lst.updown})
if (lst.schedule_list != ''):
	list_of_chats =loads(lst.schedule_list)
	print(list_of_chats)
	fiit_dictionary.update({'schedule_chat_list':list_of_chats})
else:
	fiit_dictionary.update({'schedule_chat_list':[]})
fiit_dictionary.update({'last_upd_id':lst.last_update_id})
fiit_dictionary.update({'init_week':lst.init_week})
fiit_dictionary.update({'restart_count':lst.restart_count+1})
fiit_dictionary.update({'send_schedule_bool':lst.send_schedule_bool})

if fiit_dictionary['updown']=='up':
	schedule = fiitinfo.schedule_up
else:
	schedule = fiitinfo.schedule_down


"""Сразу записываем в бд изменённый счётчик рестартов"""
write_2_db(fiit_dictionary)


#Получаем время для рассылки расписания Время Московское
servertz = pytz.timezone("Europe/Moscow")
# Определяем функцию отдельного потока
def delivery(text):
	global fiit_dictionary
	print('thread1 start and then...')
	servertz = pytz.timezone("Europe/Moscow")
	while True:
			# Переманная текущего дня и времени по Москве
			now = datetime.datetime.now(servertz)
			if (now.weekday() in range(6)) and (now.hour == 13) and (not fiit_dictionary['send_schedule_bool']) and (now.minute == 30):
				for i in fiit_dictionary['schedule_chat_list']:
					#talk2telegramapi.send_message(i, 'Можно отписаться до осени!:) А завтра в 14.30 выпить пивка!')
					talk2telegramapi.send_message(i, 'Неделя = '+fiit_dictionary['updown'])
					talk2telegramapi.send_message(i, ','.join(schedule[now.weekday()]))
				fiit_dictionary['send_schedule_bool'] = True
				write_2_db(fiit_dictionary)
			# Смена типа недели.
			if now.weekday() == 6 and now.hour ==23 and now.minute ==59 and now.second >= 55:
				if (fiit_dictionary['updown']=='up'):
					fiit_dictionary['updown']='down'
				else:
					fiit_dictionary['updown']='up'
				write_2_db(fiit_dictionary)
				sleep(10)#Избегаем повторноо переключения недели. Изменение этой перевнной должно быть 1 раз в неделю

			# В 23 часу сбрасываем флаг отправки расписания
			if now.weekday() in range(5) and now.hour == 16 and fiit_dictionary['send_schedule_bool']:
				fiit_dictionary['send_schedule_bool'] = False
				write_2_db(fiit_dictionary)

# Создаём и стартуем отдельный поток
thread1 = Thread(target=delivery,args=('',))
thread1.deamon=True
thread1.start()





# Создаём переменную с экземпляром flask
app = Flask(__name__)

#Начало маршрутов веб сервера
@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/'+misc.token+'/in', methods=['POST','GET'])
def update_in():
	global fiit_dictionary, schedule, cur, conn
	if request.method == 'POST' :
		r=request.get_json()
		try:
			message ={'update_id':r['update_id'], 'chat_id':r['message']['chat']['id'],'text':r['message']['text']}
		except Exception as e:
			print(e)
			print(r)
			message ={'update_id':1, 'chat_id':'169294743','text':'ОщиПка'}
		#talk2telegramapi.send_message(r['message']['chat']['id'],json.dumps(message, ensure_ascii=False))

		if message:
			fiit_dictionary['last_upd_id'] = message['update_id']
			write_2_db(fiit_dictionary)

			# Присваиваем переменным значения из вновь пришедшего сообщения
			msg_text = message['text']
			msg_chat_id = str(message['chat_id'])
			print(type(msg_chat_id))

			# Переписываем выбор команды
			if msg_text in fiitinfo.dict_of_commands:
				# Инизиализация и остановка рассылки расписания
				if (msg_text == '/schedule_init' or msg_text == '/schedule_init@FiitRndBot'):
					fiit_dictionary=do_schedule_init(msg_chat_id,fiit_dictionary)

				elif (msg_text == '/schedule_stop' or msg_text == '/schedule_stop@FiitRndBot'):
					fiit_dictionary=do_schedule_stop(msg_chat_id,fiit_dictionary)

				# Инизиализация типа недели
				elif (msg_text == '/init_up' or msg_text == '/init_up@FiitRndBot'):
					schedule=do_init_up(msg_chat_id)


				elif (msg_text == '/init_down' or msg_text == '/init_down@FiitRndBot'):
					schedule=do_init_down(msg_chat_id)


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
						grouplist += i['firstname']+' '+i['surname']+' '+i['patronymic']+' '+'\n'+i['phone']+'\n'+'Номер в журнале : '+i['journal_number']+'\n'+'\n'
					talk2telegramapi.send_message(msg_chat_id,grouplist)

				elif (msg_text == '/schedule_week' or msg_text == '/schedule_week@FiitRndBot'):
					schedule_week = ''
					for i in range(0,6):
						schedule_week += fiitinfo.week_days[i]+'\n'+ str(schedule[i]) +'\n'+'\n'
					talk2telegramapi.send_message(msg_chat_id,schedule_week)

				elif (msg_text == '/vars' or msg_text == '/vars@FiitRndBot'):
					print('schedule_chat_list= ',fiit_dictionary['schedule_chat_list'])
					print('updown= ',fiit_dictionary['updown'])
					print('send_schedule_bool= ',fiit_dictionary['send_schedule_bool'])
					print('schedule= ',schedule)
					print('restart_count= ',fiit_dictionary['restart_count'])
					now = datetime.datetime.now(servertz)
					print('Время на сервере ',now)


				# Тут команда с погодой
				elif (msg_text == '/weather' or msg_text == '/weather@FiitRndBot'):
					talk2telegramapi.send_message(msg_chat_id,jokeAndWeather.weather_from_darksky())

				# а тут и анекдот подъедет )
				elif (msg_text == '/joke' or msg_text == '/joke@FiitRndBot'):
					talk2telegramapi.send_message(msg_chat_id,jokeAndWeather.joke())

				# Тренируем английский
				elif (msg_text == '/train_verbs' or msg_text == '/train_verbs@FiitRndBot'):
					talk2telegramapi.send_message(msg_chat_id,train_verbs.rand_sentence()[0])

				else:
					talk2telegramapi.send_message(msg_chat_id,'Кто-то забыл прописать функцию для команды.')

			else:
				talk2telegramapi.send_message(message['chat_id'],'Не в списке команд')





		return 'OK'
	else:
		return 'HollaWord'


# Если запущен главным этот скрипт, то запускаем сервер
if __name__ == '__main__':
	port = int(environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)


#Закрываем сессию работы с бд
session.close()
