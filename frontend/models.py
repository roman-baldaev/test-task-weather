from django.db import models


class City(models.Model):
    """

    Table of cities.

    """
    city_name = models.CharField(max_length=256)

    def __str__(self):
        return str(self.id) + ' ' + str(self.city_name)


class History(models.Model):
    """

    Table of history request for auto update.

    """
    city = models.ForeignKey('City', on_delete = models.CASCADE, null = True, default = None)
    temp_values = models.TextField()
    created = models.DateTimeField(auto_now_add = True, auto_now = False)

    def __str__(self):
        return str(self.city) + ' ' + str(self.temp_values) + ' ' + str(self.created)
