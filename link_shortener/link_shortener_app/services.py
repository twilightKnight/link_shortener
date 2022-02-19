from .models import LinkReferences, HASH_LEN, UserData, VerificationCodes, CODE_LEN
from django.core.mail import send_mail
from django.conf import settings
import hashlib
import string
import random


def get_client_ip(request):
    """Retrieve IP from request"""

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def verify_email(verification_code: str):
    """Sets email verification flag to verified based on verification code received"""

    error, email = None, None
    try:
        user = VerificationCodes.objects.get(code=verification_code).user
        user.verified = True
        user.save()
        email = user.email
    except VerificationCodes.DoesNotExist:
        error = {'Invalid_Verification_Code': 'true'}
    return error, email


def send_verification_email(email: str = 'example@mail.com'):
    """Creates email verification code, stored in DB, and sends it to provided email"""

    code = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(CODE_LEN)])
    link = settings.SITE_DOMAIN_NAME + 'verification/?code=' + code
    user = UserData.objects.get(email=email)
    VerificationCodes(user=user, code=code).save()
    message = 'To verify your email follow the link below. \n' + link
    sent_flag = 0
    while sent_flag != 1:
        sent_flag = send_mail(
            'Link Shortener Verification Email',
            message,
            settings.OFFICIAL_EMAIL,
            [email],
            fail_silently=False,
        )


def check_userdata(email: str, password: str):
    """Check if entered login+password match stored ones"""

    try:
        current_user_data = UserData.objects.get(email=email)
    except UserData.DoesNotExist:
        return {'Email_Not_Exists': 'true'}

    hashed_password = _hash(current_user_data.salt, password)
    if current_user_data.password != hashed_password:
        return {'Wrong_Password': 'true'}
    return None


def save_userdata(email: str, password: str):
    """Save login, hashed+salted password"""

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


def _hash(salt: str, password: str):
    """Calculate hash of salted password"""

    salted_password = password + salt
    hashed_password = hashlib.sha256(salted_password.encode('UTF-8')).hexdigest()
    return hashed_password


def create_new_short_link(link: str = 'https://longlong_link.com', email: str = 'example@example.com'):
    """Generate short link for provided long link"""

    error = None

    # check if short link already exists
    short_link = get_existing_short_link_by_link(link)
    if short_link is not None:
        short_link = settings.SITE_DOMAIN_NAME + short_link
        return short_link, error

    short_link = generate_unique_link()

    if email is not None:
        user = UserData.objects.get(email=email)
    else:
        user = None

    LinkReferences(user=user, link=link, short_link=short_link).save()
    try:
        LinkReferences.objects.get(short_link=short_link)
    except LinkReferences.DoesNotExist:
        error = {"DB_Access_Error": "true"}

    short_link = settings.SITE_DOMAIN_NAME + short_link
    return short_link, error


def get_existing_short_link_by_link(link: str):
    """Find existing short link by long link"""

    try:
        link_object = LinkReferences.objects.get(link=link)
    except LinkReferences.DoesNotExist:
        return None
    else:
        return link_object.short_link


def generate_unique_link():
    """Generate new unique short link"""

    link = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(int(settings.SHORT_LINK_LEN))])
    # check if generated short link already exists
    try:
        LinkReferences.objects.get(short_link=link)
    except LinkReferences.DoesNotExist:
        return link
    generate_unique_link()
