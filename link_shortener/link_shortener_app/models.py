from django.db import models

HASH_LEN = 64


class LinkReferences(models.Model):
    link = models.CharField(max_length=500)
    short_link = models.CharField(max_length=8, default="")

    def __str__(self):
        return str(self.link) + '->' + str(self.short_link)


class UserData(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=HASH_LEN)
    salt = models.CharField(max_length=HASH_LEN)
