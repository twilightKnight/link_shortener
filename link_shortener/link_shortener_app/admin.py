from django.contrib import admin
from .models import UserData, LinkReferences, VerificationCodes, ClickerIPs as ips

admin.site.register([UserData, LinkReferences, VerificationCodes, ips])
