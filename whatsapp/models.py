from django.db import models

class LastAlert(models.Model):
    datetime = models.DateTimeField()
    
    def __str__ (self):
        return str(self.datetime)
    