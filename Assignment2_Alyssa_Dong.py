"""
This is an assignment that tests the use of django shell
"""
from django.contrib.auth import get_user_model
from django.db.models import Count

from blog.models import Comment, Post

User = get_user_model()

def question_1_return_active_users():
    """
    Return the results of a query which returns a list of all
    active users in the database.
    """
    return User.objects.filter(is_active = True)

def question_2_return_regular_users():
    """
    Return the results of a query which returns a list of users that
    are *not* staff and *not* superusers
    """
    return User.objects.exclude(is_superuser = True, is_staff = True)


def question_3_return_all_posts_for_user(user):
    """
    Return all the Posts authored by the user provided. Posts should
    be returned in reverse chronological order from when they
    were created.
    """
    username = User.objects.get(username = user)
    return username.blog_posts.all()


def question_4_return_all_posts_ordered_by_title():
    """
    Return all Post objects, ordered by their title.
    """
    return Post.objects.order_by('title')

def question_5_return_all_post_comments(post):
    """
    Return all the comments made for the post provided in order
    of last created.
    """
    return Comment.objects.filter(post_id = post).order_by('updated')

def question_6_return_the_post_with_the_most_comments():
    """
    Return the Post object containing the most comments in
    the database. Do not concern yourself with approval status;
    return the object which has generated the most activity.
    """
    return Post.objects.alias(
        num_comments = Count('comments')
        ).order_by('-num_comments')[:1]

def question_7_create_a_comment(post):
    """
    Create and return a comment for the post object provided.
    """
    posts = Post.objects.get(id = post)
    Comment.objects.create(post=posts)

def question_8_set_approved_to_false(comment):
    """
    Update the comment record provided and set approved=False
    """
    Comment.objects.filter(id = comment).update(status = 'draft')

def question_9_delete_post_and_all_related_comments(post):
    """
    Delete the post object provided, and all related comments.
    """
    posts = Post.objects.filter(id = post)
    comments = Comment.objects.filter(post_id = post)
    comments.delete()
    posts.delete()
