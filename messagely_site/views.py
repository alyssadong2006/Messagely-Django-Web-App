"""What the users will see"""
from django.http import HttpResponse

def index(response):
    """print hello on the screen"""
    return HttpResponse('Hello!!')
