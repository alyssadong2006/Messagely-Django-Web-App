from model_bakery import baker
import pytest

from blog.models import Post

def test_authors_included_in_context_data(client, django_user_model):
    """
    Checks that a list of unique published authors is included in the
    context and is ordered by first name.
    """
    # Make a published author called Cosmo
    cosmo = baker.make(
        django_user_model,
        username='ckramer',
        first_name='Cosmo',
        last_name='Kramer'
    )
    baker.make(
        'blog.Post',
        status=Post.PUBLISHED,
        author=cosmo,
        _quantity=2
    )
    # Make a published author called Elaine
    elaine = baker.make(
        django_user_model,
        username='ebenez',
        first_name='Elaine',
        last_name='Benez'
    )
    baker.make(
        'blog.Post',
        status=Post.PUBLISHED,
        author=elaine,
    )

    # Make an unpublished author
    unpublished_author = baker.make(
        django_user_model,
        username='gcostanza'
    )
    baker.make('blog.Post', author=unpublished_author, status=Post.DRAFT)

    # Expect Cosmo and Elaine to be returned, in this order
    expected = [cosmo, elaine]

    # Make a request to the home view
    response = client.get('/')

    # The context is available in the test response.
    result = response.context.get('authors')

    # Cast result (QuerySet) to a list to compare
    assert list(result) == expected