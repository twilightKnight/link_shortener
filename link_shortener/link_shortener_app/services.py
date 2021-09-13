from .models import LinkReferences, HASH_LEN, UserData
from django.conf import settings
import hashlib
import string
import random


def check_userdata(email, password):
    try:
        current_user_data = UserData.objects.get(email=email)
    except UserData.DoesNotExist:
        return {'Email_Not_Exists': 'true'}

    hashed_password = _hash(current_user_data.salt, password)
    if current_user_data.password != hashed_password:
        return {'Wrong_Password': 'true'}
    return None


def save_userdata(email, password):
    error = None
    try:
        UserData.objects.get(email=email)
    except UserData.DoesNotExist:
        pass
    else:
        return {"Email_Already_Used": "true"}

    salt = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(HASH_LEN - len(password))])
    hashed_password = _hash(salt, password)
    UserData(email=email, password=hashed_password, salt=salt).save()
    try:
        UserData.objects.get(email=email)
    except UserData.DoesNotExist:
        error = {"DB_Access_Error": "true"}
    return error


def _hash(salt, password):
    salted_password = password + salt
    hashed_password = hashlib.sha256(salted_password.encode('UTF-8')).hexdigest()
    return hashed_password


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
    link = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(int(settings.SHORT_LINK_LEN))])
    try:
        LinkReferences.objects.get(short_link=link)
    except LinkReferences.DoesNotExist:
        return link
    generate_unique_link()
