from django.shortcuts import redirect, render, get_object_or_404
from django.urls import NoReverseMatch

from .models import LinkReferences
from .forms import LongLinkForm, ShortLinkForm, RegistrationForm, SignInForm
from .services import create_new_short_link, save_userdata, check_userdata


def index(request):
    context = {}
    long_link_form = LongLinkForm()
    context.update({'long_link_form': long_link_form})

    try:
        user_session = request.session['username']
        context.update({'User_Session': user_session})
    except KeyError:
        user_session = None

    if request.method == 'POST':

        long_link_form = LongLinkForm(request.POST)
        if long_link_form.is_valid():

            short_link, error = create_new_short_link(long_link_form.data['long_link'])
            if error is not None:
                context.update(error)
                return render(request, 'link_shortener_app/index.html', context)

            long_link = long_link_form.data['long_link']

            long_link_form = LongLinkForm(initial={'long_link': long_link})
            context.update({'long_link_form': long_link_form})
            short_link_form = ShortLinkForm(initial={'short_link': short_link})
            context.update({'short_link_form': short_link_form})
        else:
            context.update({"Invalid_Link_Error": "true"})
        return render(request, 'link_shortener_app/index.html', context)
    elif request.method == 'GET':
        if request.GET.get('action') == 'logout' and (user_session is not None):
            del request.session['username']
            return redirect('link_shortener_app:index')

    return render(request, 'link_shortener_app/index.html', context)


def redirect_(request, short_link):
    context = {}
    long_link_form = LongLinkForm()
    context.update({'long_link_form': long_link_form})

    long_link = get_object_or_404(LinkReferences, short_link=short_link)

    try:
        return redirect(long_link.link)
    except NoReverseMatch:
        context.update({"Redirect_Error": "true"})
        return render(request, 'link_shortener_app/index.html', context)


def page_404(request, *args, **kwargs):
    return render(request, '404_page.html')


def features(request):
    context = {}
    return render(request, 'link_shortener_app/features.html', context)


def user_page(request):
    context = {}
    try:
        context.update({'User_Name': request.session['username']})
    except KeyError:
        return redirect('link_shortener_app:index')
    return render(request, 'link_shortener_app/user_page.html', context)


def create_new_user_account(request):
    context = {}
    registration_form = RegistrationForm()
    context.update({'registration_form': registration_form})

    if request.method == 'POST':

        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():

            email = registration_form.data['email']
            password = registration_form.data['password']

            if password != registration_form.data['password_confirmation']:
                context.update({"Confirmation_Error": "true"})
            else:
                error = save_userdata(email, password)
                if error is not None:
                    context.update(error)
                else:
                    request.session['username'] = email
                    return redirect('link_shortener_app:user_page')
        else:
            context.update({"Invalid_Email": "true"})

    return render(request, 'link_shortener_app/register.html', context)


def sign_in_account(request):
    context = {}
    sign_in_form = SignInForm()
    context.update({'sign_in_form': sign_in_form})

    if request.method == 'POST':

        sign_in_form = SignInForm(request.POST)
        if sign_in_form.is_valid():

            email = sign_in_form.data['email']
            password = sign_in_form.data['password']

            error = check_userdata(email, password)
            if error is not None:
                context.update(error)
            else:
                request.session['username'] = email
                return redirect('link_shortener_app:user_page')
        else:
            context.update({"Invalid_Email": "true"})
    return render(request, 'link_shortener_app/sign_in.html', context)
