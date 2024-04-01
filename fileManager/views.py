from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required
def files_page(request):
    user = request.user
    email = user.email
    return render(request, 'files.html', {'user': user})