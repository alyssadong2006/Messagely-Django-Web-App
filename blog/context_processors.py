"""
A context processor is a function which takes a single argument
 (the HttpRequest instance) and returns a dictionary.
A Django project can include any amount of processors – a 
few are declared by default by the framework in settings.py.

Register them into the settings.TEMPLATES manually
"""
from django.db.models import Count
from . import models

def base_context(request):
    """replaces contextMin, helps minimize repetitive code"""
    authors = models.Post.objects.get_authors()
    #change to pass tests --> authors =
    #   models.Post.objects.published().get_authors().order_by('first_name')
    mess_topics = models.Topic.objects.annotate(total_posts = \
                                                Count('blog_posts')).values('name', 'total_posts')
    topics_base = mess_topics.order_by('total_posts').reverse()

    return {'authors':authors, 'topics_base':topics_base}
