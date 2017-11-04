from urllib import request, parse
from bs4 import BeautifulSoup


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

        if (temp_value[0] == '-') or (ord(temp_value[0]) == 8722):
            temp = float(temp_value[1:]) * (-1)
        else:
            temp = float(temp_value)
        return temp


    except Exception as connection_error:
        return connection_error
print(yandex('Tomsk'))