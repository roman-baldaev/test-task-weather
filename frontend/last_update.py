from django.http import HttpResponse
import datetime
import psycopg2
import pytz
import json


def last_update_temperature(city):
    """A script to retrieve data from the last update.

       First check the availability of the city in the database - if not,
       then the error 404 and JSON with error and reason.

       If the city is in the database - sort by the time of the addition and select the last entry.
       Return JSON with the results, code 200.

       If the error connecting to the database is a response
       with the code 500 and the cause of the error in JSON.

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

        #if there is no city in the database
        if len(city_id) == 0:
            data = {
                'Error': 'Error in last update function.',
                'Time': str(datetime.datetime.now(utc_timezone)),
                'Reason': 'Please, check city name: {}'.format(city)
            }
            json_data_error = json.dumps(data)
            response = HttpResponse(json_data_error, status=404, content_type='application/json', charset='utf-8')
            return response
        city_id = city_id[0][0]

        #get last update
        cursor.execute(
            "SELECT temp_values, created FROM frontend_history \
              WHERE city_id = {} ORDER BY created;".format(city_id)
        )
        last_update = cursor.fetchall()[-1]
        temperature = json.loads(last_update[0])
        data = {
            'Time': str(last_update[1].astimezone(utc_timezone)),
            'Temperature': temperature,

        }
        json_data = json.dumps(data)
        response = HttpResponse(json_data, status=200, content_type='application/json', charset='utf-8')
        return response


    except Exception as connection_db_error:
        data = {
            'Error': 'Error in last update function.',
            'Time': str(datetime.datetime.now(utc_timezone)),
            'Reason': '{}'.format(connection_db_error)
        }
        json_data_error = json.dumps(data)
        response = HttpResponse(json_data_error, status=500, content_type='application/json', charset='utf-8')
        return response
    connect.close()
