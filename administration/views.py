from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from userAuth.backends import EmailBackend
from fileManager.models import File
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings


# Create your views here.
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        context = {"data": request.POST}

        
        user = EmailBackend().authenticate(request, username=email, password=password)

        
        if user is not None:
            if not user.is_staff:
                messages.add_message(request, messages.ERROR, 'User not authorized')
                context['has_error']=True
                return redirect('admin_login')
            else:
                login(request, user)
                return redirect('files')
            
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("User does not exist."))
            return redirect('admin_login')

    else:
        return render(request, 'admin/signin.html', {})
    

@login_required
@staff_member_required
def files(request):
    user = request.user
    files = File.objects.all()
    if request.method == 'POST':
        query = request.POST.get('query')
        files = File.objects.search(query=query)
        return render(request, 'admin/files.html', {'user': user, 'files': files, 'query': query})
    else:
        return render(request, 'admin/files.html', {'user': user, 'files': files})
    
@login_required
@staff_member_required
def upload_file(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        uploaded_file = request.FILES['file']

        file_instance = File.objects.create(title=title, description=description, file=uploaded_file)
        file_instance.save()

        with open(os.path.join(settings.MEDIA_ROOT, uploaded_file.name), 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        return redirect('/administration/files/')
    else:
        return render(request, 'admin/fileupload.html')
