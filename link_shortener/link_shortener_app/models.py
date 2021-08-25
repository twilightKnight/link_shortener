from django.db import models


class LinkReferences(models.Model):
    link = models.CharField(max_length=500)
    short_link = models.CharField(max_length=8, default="")

    def __str__(self):
        return str(self.link) + '->' + str(self.short_link)
