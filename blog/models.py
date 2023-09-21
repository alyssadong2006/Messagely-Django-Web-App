"""
This is the model.py for the messagely site
"""
#from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User

class PostQuerySet(models.QuerySet):
    """creating managers"""
    def published(self):
        """.published() function"""
        return self.filter(status=self.model.PUBLISHED)

    def drafts(self):
        """.drafts() function"""
        return self.filter(status=self.model.DRAFT)
    def get_authors(self):
        """.get_authors() function"""
        user = get_user_model()
        return user.objects.filter(blog_posts__in=self).distinct()


class Topic(models.Model):
    """
    Represents a topic
    """
    name = models.CharField(
        max_length = 50,
        unique= True
    )
    slug = models.SlugField(unique = True)
    def __str__(self):
        return str(self.name)
    class Meta:
        """
        ordering by name
        """
        ordering = ['name']

    def get_absolute_url(self):
        """url for topics"""
        kwargs = {'slug': self.slug,}
        return reverse('topic-detail', kwargs=kwargs)
        # if self:
        #     kwargs = {'slug': self.slug}
        # else:
        #     kwargs = {'name': self.name}
        # return reverse('topic-detail', kwargs = kwargs)
    #above is a tryout to fix bug

class Post(models.Model):
    """
    Represents a blog post
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(
        null=False,
        unique_for_date='published',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='blog_posts',
        null=False,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
    )
    content = models.TextField()
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    topics = models.ManyToManyField(
        Topic,
        related_name = 'blog_posts'
    )

    objects = PostQuerySet.as_manager()
    #content = RichTextUploadingField()

    class Meta:
        """
        ordering method
        """
        ordering = ['-created']

    def __str__(self):
        return str(self.title)

    #generating URL's
    def get_absolute_url(self):
        """url for posts, detail view"""
        if self.published:
            kwargs = {
                'year': self.published.year,
                'month': self.published.month,
                'day': self.published.day,
                'slug': self.slug
            }
        else:
            kwargs = {'pk': self.pk}

        return reverse('post-detail', kwargs=kwargs)

class Comment(models.Model):
    """
    Represents a comment
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Unapproved'),
        (PUBLISHED, 'Approved')
    ]
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='comments',
        null=True,
    )
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        related_name = 'comments',
        null = True
    )

    email = models.EmailField(blank = False)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "Approved" to make this post publicly visible',
    )
    published = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    # likes = models.ManyToManyField(User, related_name= 'comments_two')
    # dislikes = models.ManyToManyField(User, related_name = 'comments_three')
    likes = models.IntegerField(default = 0)
    dislikes = models.IntegerField(default = 0)

    def __str__(self):
        return self.comment_text[:50]
        #pylint shows this is unsubscriptable, but it is?

class Contest(models.Model):
    """
    Represents a contest submission
    """
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField()
    photo = models.ImageField(
        blank=True,
        null=True,
    )
    submitted = models.DateTimeField(auto_now_add= True)
    class Meta:
        """
        ordering of contest submissions
        """
        ordering = ['-submitted']
    def __str__(self):
        return f'{self.submitted.date()}: {self.email}'
    