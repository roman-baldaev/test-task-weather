import psycopg2
from urllib import request, error
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
import datetime
import pytz
import json


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

        # проверяем отрицательное знач-е
        if (temp_value[0] == '-') or (ord(temp_value[0]) == 8722):
            temp = float(temp_value[1:]) * (-1)
        else:
            temp = float(temp_value)
        return [temp, url]
    except Exception as connection_error:
        return [connection_error, url]


def open_weather_map(city):
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=c7365fbce4cdaa0eed49c8adb6828336'.format(city)
        req = requests.get(url)
        temperature = float(req.json()['main']['temp']) - 273.15
        return [round(temperature, 1), url]

    except Exception as connection_error:
        return [connection_error, url]


def auto_update_function(cities):
    """
        Script for autoupdate of weather

    """
    try:
            connect = psycopg2.connect(database = 'django_test', user = 'roman',
                                       host = 'localhost', password = 'admin')
            cursor = connect.cursor()
            cursor.execute(
                'SELECT city_name FROM frontend_city;'
            )
            utc_timezone = pytz.timezone('UTC')

            #read current city list from database
            cities_list = []
            cities_cursor = cursor.fetchall()

            #list of tuple to just list
            for i in range(len(cities_cursor)):
                cities_list.append(cities_cursor[i][0])

            for i in range(len(cities)):

                yandex_value = yandex(cities[i])
                open_weather_value = open_weather_map(cities[i])

                # error in yandex source
                if type(yandex_value[0]) == error.HTTPError:
                    data = {
                        'Error': 'Error in auto update function.',
                        'Time': str(datetime.datetime.now(utc_timezone)),
                        'Reason': '{}. Please, check url: {}'.format(yandex_value[0], yandex_value[1])
                    }
                    json_data_error = json.dumps(data)
                    response = HttpResponse(json_data_error, status=500, content_type='json', charset='utf-8')
                    return response

                # error in open weather source
                elif (type(open_weather_value[0]) == error.HTTPError):
                    data = {
                        'Error': 'Error in auto update function.',
                        'Time': datetime.datetime.now(utc_timezone),
                        'Reason': '{}. Please, check url: {}'.format(open_weather_value[0], open_weather_value[1])
                    }
                    json_data_error = json.dumps(data)
                    response = HttpResponse(json_data_error, status=500, content_type='json', charset='utf-8')
                    return response

                #If the city has not been checked before
                elif (cities[i] not in cities_list):
                    cursor.execute("INSERT INTO frontend_city (city_name) values ('{}');".format(cities[i]))
                    connect.commit()
                data = {
                    'Yandex': str(yandex_value[0]),
                    'Open weather': str(open_weather_value[0])
                }
                cursor.execute("SELECT id FROM frontend_city WHERE city_name = '{}';".format(cities[i]))
                city_id = cursor.fetchall()
                city_id = city_id[0][0]
                json_data = json.dumps(data)
                cursor.execute(
                    "INSERT INTO frontend_history (city_id, temp_values, created) \
                       VALUES ({},'{}', '{}');".format(city_id, json_data,
                                                       datetime.datetime.now(utc_timezone)))
                connect.commit()
            connect.close()
            response = HttpResponse(status=200, content_type='text/html', charset='utf-8')
            return response
            # cursor.execute('SELECT created FROM frontend_history WHERE city_id = 1;')
            # time = cursor.fetchall()
            #
            # times = []
            # for i in range(len(time)):
            #
            #     add = time[i][0]
            #     times.append(add)
            #
            #
            # print(times[0])
            # print ( datetime.datetime.now(utc) - times[0])
            #
            # print(datetime.datetime.now(utc) - times[0])
            # print(datetime.datetime.now(utc))
            # print(datetime.datetime.now(utc).replace(hour=datetime.datetime.now(utc).hour+1))
    except Exception as connection_db_error:
        print('Error auto_update function: {}'.format(connection_db_error))
        return connection_db_error
    connect.close()


def last_update_temperature(city):
    """A script to retrieve data from the last update.

    """
    try:
        #connect to DB
        utc_timezone = pytz.timezone('UTC')
        connect = psycopg2.connect(database='django_test', user='roman',
                                   host='localhost', password='admin')
        cursor = connect.cursor()
        #get city id
        cursor.execute("SELECT id FROM frontend_city WHERE city_name = '{}';".format(city))
        city_id = cursor.fetchall()
        city_id = city_id[0][0]

        #get last update
        cursor.execute(
            "SELECT temp_values, created FROM frontend_history \
              WHERE city_id = {} ORDER BY created;".format(city_id)
        )
        last_update = cursor.fetchall()[-1]
        return last_update

    except Exception as connection_db_error:
        print('Error last_update_temperature function: {}'.format(connection_db_error))
        return connection_db_error
    connect.close()


if __name__ == '__main__':
    utc_timezone = pytz.timezone('UTC')
    # print(yandex('Moscow'))
    # print(auto_update_function(['Moscow', 'Novosibirsk', 'Washington', 'Samara', 'Tomsk']))
    print(last_update_temperature('Tomsk'))
    # print (last_update_temperature('Tomsk')[1](utc_timezone))
    print(last_update_temperature('Tomsk')[1].astimezone(utc_timezone))
    # print(last_update_temperature('Tomsk')[1](utc_timezone))