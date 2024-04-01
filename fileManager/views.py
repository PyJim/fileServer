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
        # files = File.objects.all()
        files = [
            {
                'id': 'id',
                'title': 'How to Bake a Cake',
                'description': 'Learn step-by-step instructions on baking a delicious cake.',
                'path': 'cake.jpg',
                'date': 'January 3, 2023',
                'file_type': 'Image',
                'downloads_count': 5,
                'emailed_count': 7,
            },
            {
                'id': 'id',
                'title': '10 tips for fitness',
                'description': 'Discover essential tips for maintaining a healthy fitness routine.',
                'path': 'fit.jpg',
                'date': 'June 3, 2023',
                'file_type': 'Document',
                'downloads_count': 3,
                'emailed_count': 2,
            },
            {
                'id': 'id',
                'title': 'Introduction to AI',
                'description': 'Explore the basics of Artificial Intelligence and its applications.',
                'path': 'ai.jpg',
                'date': 'January 3, 2023',
                'file_type': 'Document',
                'downloads_count': 4,
                'emailed_count': 1,
            }
        ]
        return render(request, 'files.html', {'user': user, 'files': files})