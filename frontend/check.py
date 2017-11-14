"""
Module for check city name.

"""

def check(city):
    if type(city) != str:
        return False
    if city == '':
        return False
    for i in city:
        if (ord(i) >= 65 and ord(i) <= 90) or (ord(i) >= 97 and ord(i) <= 122) or (i == '-'):
            pass
        else:
            return False
    return True
a = input()
a = a.replace(' ', '-')
if (check(a)):
    print('Good')
else:
    print('Bad...')
print(a)