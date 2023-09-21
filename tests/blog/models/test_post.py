from model_bakery import baker
from blog.models import Post

def test_get_authors_returns_unique_users(django_user_model):
    # Create a user
    author = baker.make(django_user_model)
    # Create multiple posts. The _quantity argument can be used
    # to specify how many objects to create.
    baker.make('blog.Post', author=author, _quantity=3)

    assert list(Post.objects.get_authors()) == [author]