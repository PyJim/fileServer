from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from validate_email import validate_email
from .models import User
from .backends import EmailBackend
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    
    def run(self):
        self.email.send()


# Create your views here.
def send_activation_email(user, request):
    current_site =get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('authenticate/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(
        subject=email_subject, 
        body=email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[user.email],

    )

    EmailThread(email).start()



def signup(request):
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'Password must be at least 6 characters')
            context['has_error']=True
        
        if password != confirm_password:
            messages.add_message(request, messages.ERROR, 'Passwords do not match')
            context['has_error']=True
        
        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Enter a valid email address')
            context['has_error']=True
        

        # check if email is already taken
        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email already taken')
            context['has_error']=True
        
        if context['has_error']:
            return render(request, 'authenticate/signup.html', context)
        

        # create the user
        user = User.objects.create_user(email=email, password=password)
        # add a success message

        send_activation_email(user, request)

        messages.add_message(request, messages.SUCCESS, 'Please check your email to verify your account')
        # redirect to login page
        return redirect('login')

    else:
        return render(request, 'authenticate/signup.html')
    

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        context = {"data": request.POST}

        
        user = EmailBackend().authenticate(request, username=email, password=password)

        if not user.is_email_verified:
            messages.add_message(request, messages.ERROR, 'Email is not verified. Kindly check your inbox')
            context['has_error']=True

            return render(request, "authenticate/login.html", context)

        if user is not None:
            login(request, user)
            url = '/fileManager/'
            return redirect(url)
            
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("There was an error logging in. Try again."))
            return redirect('login')

    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    return HttpResponse('Logout')

def activate_user(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user=None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Account Activated Successfully, You can now login')
        return redirect('login')
    
    return render(request, 'authenticate/activation_failed.html', {"user": user})



def request_activation_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)

        if user:
            if user.is_email_verified:
                messages.add_message(request, messages.SUCCESS, 'Account is already verified')
                # redirect to login page
                return redirect('login')

            send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS, 'Please check your email to verify your account')
            # redirect to login page
            return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, 'Email not found')
            return redirect('signup')
    else:
        return render(request, 'authenticate/activation_failed.html')



def reset_password(request):
    return render(request, 'reset_password.html')

def reset_password_token(request):
    return render(request, 'password_token.html')

