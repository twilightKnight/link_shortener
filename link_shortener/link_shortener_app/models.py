from django.db import models
from django.utils import timezone

HASH_LEN = 64
CODE_LEN = 50


class UserData(models.Model):
    """User account information"""

    email = models.CharField(max_length=50)
    verified = models.BooleanField(default=False)
    password = models.CharField(max_length=HASH_LEN)
    salt = models.CharField(max_length=HASH_LEN)

    def __str__(self):
        return str(self.email)


class LinkReferences(models.Model):
    """Short link, referring to long link, and its connected features"""

    user = models.ForeignKey(UserData, default=None, on_delete=models.CASCADE, blank=True, null=True)
    link = models.SlugField(max_length=500)
    short_link = models.SlugField(max_length=8, default="")
    creation_date = models.DateField(default=timezone.now)
    # for clicks counter feature
    clicks_counter_feature = models.BooleanField(default=False)
    clicks = models.IntegerField(default=None, null=True)
    # for ip tracking feature
    clicker_ip_tracker_feature = models.BooleanField(default=False)

    def __str__(self):
        return str(self.short_link)


class VerificationCodes(models.Model):
    """Codes to verify user`s email"""

    user = models.ForeignKey(UserData, on_delete=models.CASCADE, default=None)
    code = models.CharField(max_length=CODE_LEN)


class ClickerIPs(models.Model):
    """IPs of users, redirected by short link"""

    link = models.ForeignKey(LinkReferences, on_delete=models.CASCADE, default=None)
    ip = models.GenericIPAddressField()

