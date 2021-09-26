from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return render(request, 'home.html', {
        'new_item_text': request.POST.get('item_text','')})
        # request.POST['key'] : returns a key error if key doesn't exist
        # request.POST.get('key','default) : returns None if key doesn't exist or default if provided
