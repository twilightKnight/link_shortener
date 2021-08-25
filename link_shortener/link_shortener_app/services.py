from .models import LinkReferences
from django.conf import settings
import string
import random


def create_new_short_link(link):
    error = None

    short_link = get_existing_short_link_by_link(link)
    if short_link is not None:
        short_link = settings.SITE_DOMAIN_NAME + short_link
        return short_link, error

    short_link = generate_unique_link()

    LinkReferences(link=link, short_link=short_link).save()
    try:
        LinkReferences.objects.get(short_link=short_link)
    except LinkReferences.DoesNotExist:
        error = {"DB_Access_Error": "true"}

    short_link = settings.SITE_DOMAIN_NAME + short_link
    return short_link, error


def get_existing_short_link_by_link(link):
    try:
        link_object = LinkReferences.objects.get(link=link)
    except LinkReferences.DoesNotExist:
        return None
    else:
        return link_object.short_link


def generate_unique_link():
    link = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(settings.SHORT_LINK_LEN)])
    try:
        LinkReferences.objects.get(short_link=link)
    except LinkReferences.DoesNotExist:
        return link
    generate_unique_link()
