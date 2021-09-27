from django.db import models

HASH_LEN = 64
CODE_LEN = 50


class LinkReferences(models.Model):
    link = models.CharField(max_length=500)
    short_link = models.CharField(max_length=8, default="")

    def __str__(self):
        return str(self.link) + '->' + str(self.short_link)


class UserData(models.Model):
    email = models.CharField(max_length=50)
    verified = models.BooleanField(default=False)
    password = models.CharField(max_length=HASH_LEN)
    salt = models.CharField(max_length=HASH_LEN)


class VerificationCodes(models.Model):
    email = models.CharField(max_length=50)
    code = models.CharField(max_length=CODE_LEN)
