from distutils.command.clean import clean
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

#message system
from project1 import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode

#login logout
from django.contrib import messages
from . tokens import generate_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . forms import CreateUserForm



# Create your views here.
#@login_required(login_url="signin")
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                #welome email
                user = form.cleaned_data.get("username")
                user_email = form.cleaned_data.get("email")
                first_name = form.cleaned_data.get("first_name")
                form.is_active = False
                form.save()

                messages.success(request, "Acount was succesfully created for " + user)

                
                subject = "Welcome to my inspirational Blog!!"
                message = "Hello" + user + "!! \n" + "Welcome to my inspirational blog!! \n thank you for visiting my website \n we have also sent you a confirmation email \n please confirm your email with the link \n\n Thank you \n imosemi"
                from_email = settings.EMAIL_HOST_USER
                to_list = [user_email]
                send_mail(subject, message, from_email, to_list, fail_silently=True)

                return redirect("signin")

        context = {"form": form}
        return render(request, "authentication/signup.html", context)




# #Email address confirmation 
# current_site = get_current_site(request)
# email_subject = "confirm your email @ inspirational blog"
# message2 = render_to_string("email_confirmation.html", {
#     "name": first_name,
#     "domain": current_site.domain,
#     "uid": urlsafe_base64_encode(force_bytes(form)),
#     "token": generate_token.make_token(form)
# })
# email = EmailMessage(
#     email_subject,
#     message2,
#     settings.EMAIL_HOST_USER,
#     [user_email],
# )
# email.fail_silently = True
# email.send()

def signin(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username =  request.POST.get("username")
            password = request.POST.get("password")
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                messages.success(request, "you're successfully logged in. ")
                login(request, user)
                return redirect("home")

            else:
                messages.info(request, "Username OR Password is incorrect")

            
        context = {}
        return render(request, "authentication/signin.html", context)



def signout(request):
    logout(request)
    messages.success(request, "logged out succesfully")
    return redirect("home")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect("home")

    else:
        return render(request, "activation_failed.html")

