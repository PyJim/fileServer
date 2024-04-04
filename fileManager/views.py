from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import File
from .models import File
import os
import threading
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
import mimetypes



# create a thread to asyncrhonously send emails
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    
    def run(self):
        self.email.send()


# Create your views here.

@login_required
def files_page(request):
    user = request.user
    if request.method == 'POST':
        query = request.POST.get('query')
        files = File.objects.search(query)
        if not files:
            files = []

        return render(request, 'files.html', {'user': request.user, 'files': files, 'query': query})


    else:
        files = File.objects.all()
        
        return render(request, 'files.html', {'user': user, 'files': files})
    

@login_required
def email_file(request, file_id):
    if request.method =='POST':
        requested_file = File.objects.get(pk=file_id)
        file_obj = get_object_or_404(File, pk=file_id)

        to_email = request.POST.get('email')
        email_subject = requested_file.title
        email_body = 'Please find attached the file you requested.'

        email = EmailMessage(
            subject=email_subject, 
            body=email_body,
            from_email=settings.EMAIL_FROM_USER,
            to=[to_email],
        )

        # Attach the file to the email
        file_path = file_obj.file.path
        extension = os.path.splitext(file_path)[1].lower()
        mime_type, _ = mimetypes.guess_type(file_path)  # Get MIME type
        if not mime_type:
            mime_type = 'application/octet-stream'

        with open(file_path, 'rb') as file:
            email.attach(file_obj.title, file.read(), mime_type)

        # Send the email asynchronously
        EmailThread(email).start()

        # increment the number of times the file has been emailed
        requested_file.emailed_count += 1
        requested_file.save()

        messages.add_message(request, messages.SUCCESS, 'File sent successfully')

        return redirect('/feed/')
    else:
        return render(request, 'send_file.html')
    


@login_required
def files_page(request):
    user = request.user
    if request.method == 'POST':
        query = request.POST.get('query')
        files = File.objects.search(query)
        if not files:
            files = []
        return render(request, 'files.html', {'user': request.user, 'files': files, 'query': query})
    else:
        files = File.objects.all()
        return render(request, 'files.html', {'user': user, 'files': files})
    

    

@login_required
def download_file(request, file_id):
    requested_file = File.objects.get(pk=file_id)
    file_obj = get_object_or_404(File, pk=file_id)
    file_path = file_obj.file.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        requested_file.downloads_count += 1
        requested_file.save()
        return response
    

