import psycopg2
from urllib3 import request
import requests
from bs4 import BeautifulSoup
import datetime
import pytz


def yandex(city):
    try:

        myheader = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' \
                                  '(KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
        }

        url = 'https://yandex.ru/pogoda/{}'.format(city)
        req = request.Request(url, headers = myheader)
        answer = BeautifulSoup(request.urlopen(req))
        temp_value = str(answer.find('span', 'temp__value')).split('>')[1].split('<')[0]

        if (temp_value[0] == '-') or (ord(temp_value[0]) == 8722): #проверяем отрицательное знач-е
            temp = float(temp_value[1:]) * (-1)
        else:
            temp = float(temp_value)
        return temp


    except Exception as connection_error:
        return connection_error


def open_weather_map (city):
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=c7365fbce4cdaa0eed49c8adb6828336'.format(city)
        req = requests.get(url)

        return req.json()['main']['temp']

    except Exception as connection_error:
        return connection_error

#вне зависимости от приведенного числового пояса, разнима времени вычисляется корректно
def fill_auto(args):
    """
        script for autoupdate of weather
    """
    try:
        connect = psycopg2.connect(database = 'django_test', user = 'roman', host = 'localhost', password = 'admin')

        cursor = connect.cursor()

        cursor.execute('SELECT created FROM frontend_history WHERE city_id = 1;')
        time = cursor.fetchall()
        utc = pytz.timezone('UTC')
        times = []
        for i in range(len(time)):

            add = time[i][0]
            times.append(add)


        print(times[0])


        print(datetime.datetime.now(utc) - times[0])
        print(datetime.datetime.now(utc) - times[1])
    except Exception as connection_db_error:
        print('Error fill_auto function: {}'.format(connection_db_error))
        return connection_db_error

    connect.close()
if __name__ == '__main__':
    fill_auto('Tomsk')