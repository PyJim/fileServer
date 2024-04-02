from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import File


# Create your views here.

@login_required
def files_page(request):
    if request.method == 'POST':
        pass

    else:
        user = request.user
        email = user.email
        files = File.objects.all()
        
        return render(request, 'files.html', {'user': user, 'files': files})