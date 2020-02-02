from django.db import models

class APIKey(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    apikey = models.CharField(max_length=20)

    def __str__(self):
        return self.email

class JSONRecord(models.Model):
    record_id = models.CharField(max_length=10, primary_key=True)
    json_string = models.TextField()
    user_api_key = models.CharField(max_length=20)

    def __str__(self):
        return self.user_api_key
