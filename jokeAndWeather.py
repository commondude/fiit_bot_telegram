import requests
import time
import json
import random
from math import ceil, floor

# Запрос текущей погоды DarkSky
def weather_from_darksky():
    try:
        res = requests.get("https://api.darksky.net/forecast/1ac4cfdc57024c7c53126161d677d495/47.2247,39.7165?lang=ru&units=si")
        data = res.json()
        # берем текущее время с сервера в секундах:
        vrem = data['currently']['time']+10800
        # и получаем из него нормальные дату и время
        vrem = time.ctime(vrem)
        # берем описание погоды на текущий момент
        curr_weather = data['currently']['summary']
        # теперь возьмем прогноз на день
        day_weather = data['hourly']['summary']
        # и прогноз на неделю
        week_weather = data['daily']['summary']
        # берем температуру в Цельсиях:
        t_cel = data['currently']['temperature']
        # берем скорость ветра в м/с
        veter = data['currently']['windSpeed']
        veter_low = floor(veter)
        veter_high = ceil(veter)
        try:
            wind_dir = data['currently']['windBearing']
        except KeyError:
            wind_dir = 0
    except Exception as e:
        print("Exception (weather): ", e)
        pass
    output = "Время запроса: " + vrem + "\n" + "Сейчас: " + curr_weather + "\n" + "темература воздуха: " + str(t_cel) + "°C" + "\n" + "ветер: "+wind_direction(wind_dir) + str(veter_low)+"-"+str(veter_high) + " м/с"+ "\n"  +\
    "Прогноз на день: " +day_weather+ "\n" + "Прогноз на неделю: " + week_weather
    return '\n'+output+'\n'

def wind_direction(deg):
    if deg <= 23 or deg >= 338:
        return "северный "
    elif deg in range(23, 68):
        return "северо-восточный "
    elif deg in range(68, 113):
        return "восточный "
    elif deg in range(113, 158):
        return "юго-восточный "
    elif deg in range(158, 203):
        return "южный "
    elif deg in range(203, 248):
        return "юго-западный "
    elif deg in range(248, 293):
        return "западный "
    elif deg in range(293, 338):
        return "северо-западный "

#----------------------------------------------------------------------------------------------------

def joke():
	#запрос на сервер с указанием типа шутки
	res = requests.get('http://rzhunemogu.ru/RandJSON.aspx?CType=1')
	try:
		#декодируем ответ, отключив строгую проверку для декодера
		strk=json.JSONDecoder(strict=False).decode(res.content.decode('windows-1251'))
		#если всё норм,то возвращаем анекдот
		return ' анекдот \n' + strk['content']
	except:
		#эта строка для случаев,когда что-то не так с ответом и его декодированием
		strk={'content':'что-то пошло не так :( попробуй еще раз'}
	# выводим на экран результат
	return strk['content']+'\n'
