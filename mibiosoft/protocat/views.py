from django.shortcuts import *
from django.http import *

# Create your views here.
def index(request):
    context = {
        'title': 'ProtoCat'
    }
    print ("RENDERING REQUESTS")
    return render(request, 'index.html', context)