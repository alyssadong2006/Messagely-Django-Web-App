"""
This is the file responsible for controlling the data the html page can show
"""
# from typing import Any, Dict
from django.contrib import messages
from django.db import models
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, FormView, ListView, CreateView
from django.urls import reverse_lazy
#from django.db.models import Count
from django.db.models import F
from . import models, forms
#from django.http import JsonResponse
import json
# for clarity reasons, is replaced:
# def home(request):
#     ""
#     The Blog Homepage
#     ""
#     latest_posts = models.Post.objects.order_by('published').reverse()[:10]
#     mess_topics = models.Topic.objects.annotate
#         (total_posts = Count('blog_posts')).values('name', 'total_posts')
#     topics = mess_topics.order_by('total_posts').reverse()
#     authors = models.Post.objects.get_authors()
#     #to pass test:
#     # authors = models.Post.objects.published().get_authors().order_by('first_name')
#     context = {'latest_posts': latest_posts, 'topics': topics, 'authors': authors}
#     return render(request, 'blog/home.html', context)
# ____________________________________________________
# another way:
# class AboutView(View):
#     def get(self, request):
#         return render(request, 'blog/about.html')
# ____________________________________________________
# These stuff can also be moved to the context_processors:
# class ContextMixin:
#     ""
#     Provides common context variables for blog views
#     ""
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['authors'] = models.Post.objects.get_authors()
#         #change to pass tests --> authors = models.Post.objects.
#             published().get_authors().order_by('first_name')
#         mess_topics = models.Topic.objects.annotate(total_posts =
#             Count('blog_posts')).values('name', 'total_posts')
#         context['topics'] = mess_topics.order_by('total_posts').reverse()
#         return context
#class AboutView(ContextMixin, TemplateView):
class AboutView(TemplateView):
    """views for the about.html"""
    template_name = 'blog/about.html'

class ContactView(TemplateView):
    """views for the contact.html"""
    template_name = 'blog/contact.html'

#class HomeView(ContextMixin, TemplateView):
class HomeView(TemplateView):
    """views for the home.html"""
    template_name = 'blog/home.html'
    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)

        latest_posts = models.Post.objects.order_by('published').reverse()[:10]
        # Update the context with our context variables
        context.update({
            'latest_posts': latest_posts
        })

        return context

class PostListView(ListView):
    """views for the list of posts"""
    model = models.Post
    context_object_name = 'posts'#changes "object_list" to "posts", used in post_list.html for loop
    queryset = models.Post.objects.published() #shows only the published posts

class PostDetailView(DetailView): #register in URL patterns
    """views for the details of selected post"""
    model = models.Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
    # Get the base queryset
        queryset = super().get_queryset().published()
        # If this is a `pk` lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # Otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )
    
    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)
        print(self.get_object())
        comments = models.Comment.objects.filter(post = self.get_object())
        context.update({
            'comments': comments,
        })
        return context

class TopicListView(ListView):
    """views for the topic list"""
    model = models.Topic
    context_object_name = 'topics'


class TopicDetailView(DetailView):
    """views for the topic detail view (posts matching the topic)"""
    # model = models.Topic #filtering from posts

    # def get_queryset(self):
    #     #data = super().get_context_data(**kwargs)
    #     #data['posts'] = super().get_queryset.filter(topic = "Topic")
    #     queryset = super().get_queryset()
    #     #posts = Post.objects.filter(topics = queryset.first())
    #     return queryset
    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     data['posts'] = Post.objects.filter(topics_slug = self.kwargs['slug'])
    #     return data
    template_name = 'blog/topic_detail.html'
    model = models.Topic
    def get_queryset(self):
        #data = super().get_context_data(**kwargs)
        #data['posts'] = super().get_queryset.filter(topic = "Topic")
        queryset = super().get_queryset()
        #posts = Post.objects.filter(topics = queryset.first())
        return queryset

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)
        print(self.get_object())
        posts = models.Post.objects.filter(topics = self.get_object()).published()
        # Update the context with our context variables
        context.update({
            'posts': posts
        })
        return context
def terms_and_conditions(request):
    """a function that defines the views for the terms and conditions page"""
    return render(request, 'blog/terms_and_conditions.html')
# def form_example(request):
#         # Handle the POST
#     if request.method == 'POST':
#         # Pass the POST data into a new form instance for validation
#         form = forms.ExampleSignupForm(request.POST)
#         # If the form is valid, return a different template.
#         if form.is_valid():
#             # form.cleaned_data is a dict with valid form data
#             cleaned_data = form.cleaned_data
#             return render(
#                 request,
#                 'blog/form_example_success.html',
#                 context={'data': cleaned_data}
#             )
#     # If not a POST, return a blank form
#     else:
#         form = forms.ExampleSignupForm()
#     # Return if either an invalid POST or a GET
#     return render(request, 'blog/form_example.html', context={'form': form})
#replaced by code down below:
class FormViewExample(FormView):
    """
    The View for the example form
    """
    template_name = 'blog/form_example.html'
    form_class = forms.ExampleSignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Create a "success" message
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you for signing up!'
        )
        # Continue with default behaviour
        return super().form_valid(form)

class ContestFormView(CreateView):
    """
    The View for the photo contest submission
    """
    model = models.Contest
    success_url = reverse_lazy('home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'photo',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you! Your message has been sent.'
        )
        return super().form_valid(form)
# class ContactFormView(FormView):
#     template_name = 'blog/contact_form.html'
#     form_class = forms.PhotoForms
#     success_url = reverse_lazy('home')

#     def form_valid(self, form):
#         messages.add_message(
#             self.request,
#             messages.SUCCESS,
#             'Thank you! Your message has been sent.'
#         )
#         return super().form_valid(form)
class AddPostFormView(CreateView):
    """
    This view is for adding new posts
    """
    model = models.Post
    success_url = reverse_lazy('home')
    fields = [
        'author',
        'title',
        'slug',
        'published',
        'content',
        'status',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you! Your post has been sent.'
        )
        return super().form_valid(form)

def like_comment(request):
    data = json.loads(request.body)
    print(data)
    id = data["id"]
    comment = models.Comment.objects.get(id = id)
    comment.likes = F('likes') + 1
    comment.save()
    #return JsonResponse("it's working", safe = False)
    return render(request, 'blog/post_detail.html')

def dislike_comment(request):
    data = json.loads(request.body)
    print(data)
    id = data["id"]
    comment = models.Comment.objects.get(id = id)
    comment.dislikes = F('dislikes') + 1
    comment.save()
    print(comment.dislikes)
    #return JsonResponse("it's working", safe = False)
    return render(request, 'blog/post_detail.html')
