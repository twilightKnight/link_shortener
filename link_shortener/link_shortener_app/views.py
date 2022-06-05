from django.shortcuts import redirect, render, get_object_or_404
from django.urls import NoReverseMatch
from django.db import transaction
from django.views import View

from .models import LinkReferences, UserData, ClickerIPs
from .forms import LongLinkForm, ShortLinkForm, RegistrationForm, SignInForm
from .services import create_new_short_link, save_userdata, check_userdata, send_verification_email, verify_email,\
    get_client_ip


class Index(View):
    """Create your short link here"""

    context = {'long_link_form': LongLinkForm()}

    def post(self, request):
        user_session = self.get_user_session(request)

        # short link creation
        long_link_form = LongLinkForm(request.POST)
        if long_link_form.is_valid():

            short_link, error = create_new_short_link(long_link_form.data['long_link'], user_session)
            if error is not None:
                self.context.update(error)
                return render(request, 'link_shortener_app/index.html', self.context)

            long_link = long_link_form.data['long_link']

            long_link_form = LongLinkForm(initial={'long_link': long_link})
            self.context.update({'long_link_form': long_link_form})
            short_link_form = ShortLinkForm(initial={'short_link': short_link})
            self.context.update({'short_link_form': short_link_form})
        else:
            self.context.update({"Invalid_Link_Error": "true"})
        return render(request, 'link_shortener_app/index.html', self.context)

    # logout handling
    def get(self, request):
        user_session = self.get_user_session(request)
        if request.GET.get('action') == 'logout' and (user_session is not None):
            del request.session['username']
            return redirect('link_shortener_app:index')

        return render(request, 'link_shortener_app/index.html', self.context)

    def get_user_session(self, request):
        try:
            user_session = request.session['username']
            self.context.update({'User_Session': user_session})
            return user_session
        except KeyError:
            return None


class Redirect(View):
    """Redirect user by provided short link"""

    context = {'long_link_form': LongLinkForm()}

    def get(self, request, short_link):
        link = get_object_or_404(LinkReferences, short_link=short_link)

        # count clicks if feature is enabled
        if link.clicks_counter_feature:
            if link.clicks is None:
                link.clicks = 1
            else:
                link.clicks = link.clicks + 1
            link.save()

        # track IPs if feature is enabled
        if link.clicker_ip_tracker_feature:
            ClickerIPs(link=link, ip=get_client_ip(request)).save()

        # redirect itself
        try:
            return redirect(link.link)
        except NoReverseMatch:
            self.context.update({"Redirect_Error": "true"})
            return render(request, 'link_shortener_app/index.html', self.context)


class UserPage(View):
    """Authorised user`s short link management page"""

    context = {}

    def get(self, request):
        try:
            self.context.update({'User_Session': request.session['username']})
        except KeyError:
            return redirect('link_shortener_app:index')

        user = UserData.objects.get(email=request.session['username'])
        links = LinkReferences.objects.filter(user=user)
        self.context.update({'Links': links})
        return render(request, 'link_shortener_app/user_page.html', self.context)


class CreateUser(View):
    """User registration"""

    context = {'registration_form': RegistrationForm()}

    def get(self, request):
        return render(request, 'link_shortener_app/register.html', self.context)

    @transaction.atomic()
    def post(self, request):

        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():

            email = registration_form.data['email']
            password = registration_form.data['password']

            if password != registration_form.data['password_confirmation']:
                self.context.update({"Confirmation_Error": "true"})
            else:
                error = save_userdata(email, password)
                if error is not None:
                    self.context.update(error)
                else:
                    send_verification_email(email)
                    return redirect('link_shortener_app:email_verifier')
        else:
            self.context.update({"Invalid_Email": "true"})
        return render(request, 'link_shortener_app/register.html', self.context)


class EmailVerifier(View):
    """Email verification page"""

    context = {}

    def get(self, request):
        if request.GET.get('code') is not None:
            error, email = verify_email(request.GET.get('code'))
            if error:
                self.context.update(error)
            else:
                request.session['username'] = email
                self.context.update({'Email': email})
                return redirect('link_shortener_app:user_page')

        return render(request, 'link_shortener_app/verification.html', self.context)


class LinkUpdate(View):
    """Edit LinkReference object settings e.g. count clicks and track IPs flags"""

    def get(self, request, short_link: str, clicks_mode: str = 'True'):
        requester = request.session['username']
        link = LinkReferences.objects.get(short_link=short_link)
        link_owner = link.user.email
        if requester == link_owner:
            # change clicks flag
            if clicks_mode == 'True':
                link.clicks_counter_feature = not link.clicks_counter_feature
                link.save()
            # change IP flag
            else:
                link.clicker_ip_tracker_feature = not link.clicker_ip_tracker_feature
                link.save()

        return redirect('link_shortener_app:user_page')


class SignInAccount(View):
    """Authorise user and start his browser session"""

    context = {'sign_in_form': SignInForm()}

    def get(self, request):
        return render(request, 'link_shortener_app/sign_in.html', self.context)

    def post(self, request):
        sign_in_form = SignInForm(request.POST)
        if sign_in_form.is_valid():

            email = sign_in_form.data['email']
            password = sign_in_form.data['password']

            error = check_userdata(email, password)
            if error is not None:
                self.context.update(error)
            else:
                if UserData.objects.get(email=email).verified:
                    request.session['username'] = email
                    return redirect('link_shortener_app:user_page')
                else:
                    return redirect('link_shortener_app:email_verifier')
        else:
            self.context.update({"Invalid_Email": "true"})
            return render(request, 'link_shortener_app/sign_in.html', self.context)


def page_404(request, *args, **kwargs):
    """Custom 404 page"""

    return render(request, 'link_shortener_app/404_page.html', status=404)


def features(request):
    """Feature list page"""

    context = {}
    try:
        user_session = request.session['username']
        context.update({'User_Session': user_session})
    except KeyError:
        pass
    return render(request, 'link_shortener_app/features.html', context)
