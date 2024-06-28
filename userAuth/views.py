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
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import threading
from django.contrib.auth.decorators import login_required



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
    email_body = get_template('authenticate/activate.html').render({'user': user,
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
    email.content_subtype = "html"
    EmailThread(email).start()



def send_forgot_password_reset_email(request, user):
    current_site =get_current_site(request)
    email_subject = 'Reset Password'
    email_body = get_template('authenticate/password_OTP.html').render({
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
    email.content_subtype = "html"
    EmailThread(email).start()



def home(request):
    return redirect('login')


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


        if user is not None:
            if not user.is_email_verified:
                send_activation_email(user, request)
                messages.add_message(request, messages.ERROR, 'Email is not verified. Kindly check your inbox')
                context['has_error']=True

                return redirect('request_activation_email')
            
            login(request, user)
            return redirect('feed')
            
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("User does not exist."))
            return redirect('login')

    else:
        return render(request, 'authenticate/login.html', {})

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

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



@login_required
def reset_password(request):
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # get current user information
        user = request.user

        try:
            email = user.email
            user = EmailBackend().authenticate(request, username=email, password=current_password)
        except Exception as e:
            user=None
            

        if user is not None:
            if new_password != confirm_password:
                messages.add_message(request, messages.ERROR, 'Passwords do not match')
                context['has_error']=True

            else:
                user.set_password(new_password)
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Password changed successfully')
                return redirect("feed")
            
            if context['has_error']:
                return render(request, 'authenticate/reset_password.html', context)
        else:
            messages.add_message(request, messages.ERROR, 'something went wrong. Check password')
            context['has_error']=True
            return render(request, 'authenticate/reset_password.html', context)
    else:
        return render(request, 'authenticate/reset_password.html')


        
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        user = User.objects.get(email=email)

        if user is not None:
            send_forgot_password_reset_email(request=request, user=user)
            messages.add_message(request, messages.SUCCESS, 'Password reset link sent successfully. Please check your email')
            return redirect("login")
        else:
            messages.add_message(request, messages.ERROR, 'something went wrong. Please check your email')
            return render(request, 'authenticate/forgot_password.html')

    else:
        return render(request, 'authenticate/forgot_password.html')
    


def reset_forgotten_password(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user=None

    if not (user and generate_token.check_token(user, token)):
        return render(request, 'authenticate/forgot_password_reset_failed.html') 

    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'Password must be at least 6 characters')
            context['has_error']=True
        
        if password != confirm_password:
            messages.add_message(request, messages.ERROR, 'Passwords do not match')
            context['has_error']=True

        if context['has_error']:
            return render(request, 'authenticate/forgot_password_reset_failed.html', context)

        user.set_password(password)
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Password changed Successfully, You can now login')
        return redirect('login')
    
    else:
        return render(request, 'authenticate/reset_forgotten_password.html', {"data": user})