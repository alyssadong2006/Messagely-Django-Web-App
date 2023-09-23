"""
This is the messagely admin file
"""
from django.contrib import admin
from .models import Post, Comment, Topic, Contest

class CommentInline(admin.StackedInline):
    """
    Inline comments under the Posts
    """
    model = Comment
    extra = 0
    readonly_fields = ('email','author','comment_text')

class PostAdmin(admin.ModelAdmin):
    """
    How the posts will be displayed
    """
    list_display = (
        'title',
        'author',
        'status',
        'created',
        'updated',
    )

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    list_filter = (
        'status',
        'topics',
    )

    inlines = [
        CommentInline,
    ]

    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """
    How the topics will be displayed
    """
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug':('name',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    How all the comments will be displayed
    """
    list_display = (
        'author',
        'post',
        'published',
        'updated',
        'email',
        'status',
    )

    search_fields = (
        'comment_text',
    )

    list_filter = (
        'status',
    )

    date_hierarchy = 'published'

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'last_name',
        'first_name',
        'submitted'
    )

    readonly_fields = (
        'first_name',
        'last_name',
        'email',
        'submitted',
        'photo',
    )