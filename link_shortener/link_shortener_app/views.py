from django.shortcuts import redirect, render
from django.urls import NoReverseMatch
from .models import LinkReferences
from .forms import LongLinkForm, ShortLinkForm
from .services import create_new_short_link


def index(request):
    context = {}
    long_link_form = LongLinkForm()
    context.update({'long_link_form': long_link_form})

    if request.method == 'POST':

        long_link_form = LongLinkForm(request.POST)
        if long_link_form.is_valid():

            short_link, error = create_new_short_link(long_link_form.data['long_link'])
            if error is not None:
                context.update(error)
                return render(request, 'link_shortener_app/index.html', context)

            tmp = long_link_form.data['long_link']
            long_link_form = LongLinkForm(initial={'long_link': tmp})
            context.update({'long_link_form': long_link_form})
            short_link_form = ShortLinkForm(initial={'short_link': short_link})
            context.update({'short_link_form': short_link_form})
        else:
            context.update({"Invalid_Link_Error": "true"})

        return render(request, 'link_shortener_app/index.html', context)
    return render(request, 'link_shortener_app/index.html', context)


def redirect_(request, short_link):
    context = {}
    long_link_form = LongLinkForm()
    context.update({'long_link_form': long_link_form})
    try:
        long_link = LinkReferences.objects.get(short_link=short_link)
    except LinkReferences.DoesNotExist:
        context.update({"Short_link_Not_Found_Error": "true"})
        return render(request, 'link_shortener_app/index.html', context)

    try:
        return redirect(long_link.link)
    except NoReverseMatch:
        context.update({"Redirect_Error": "true"})
        return render(request, 'link_shortener_app/index.html', context)


def features(request):
    context = {}
    return render(request, 'link_shortener_app/features.html', context)


def create_new_user_account(request):
    context = {}
    return render(request, 'link_shortener_app/sign_up.html', context)


def sign_in_account(request):
    context = {}
    return render(request, 'link_shortener_app/sign_in.html', context)
