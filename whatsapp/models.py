from django.db import models

class LastAlert(models.Model):
    datetime = models.DateTimeField()

    @classmethod
    def get_last_alert(cls):
        try:
            last_alert = cls.objects.latest('id')
            return last_alert.datetime
        except cls.DoesNotExist:
            return None

    @classmethod
    def update_last_alert(cls, datetime):
        last_alert = cls.get_last_alert()
        if last_alert != datetime:
            cls.objects.create(datetime=datetime)

