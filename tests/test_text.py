import pytest
from demo.models import Artist

from adminfilters.filters import MultiValueFilter, ValueFilter


@pytest.fixture
def fixtures(db):
    from demo.factories import ArtistFactory
    ArtistFactory(name='a1')
    ArtistFactory(name='a2')
    ArtistFactory(name='b1')
    ArtistFactory(name='c1')


def test_media():
    assert ValueFilter.factory(title='Title')(None, None, {}, None, None, 'unique').media


@pytest.mark.parametrize('value,negate,expected', [('n', False, []),
                                                   ('a1', False, ['a1']),
                                                   ('a1', True, ['a2', 'b1', 'c1']),
                                                   ])
def test_value_filter(fixtures, value, negate, expected):
    f = ValueFilter(Artist._meta.get_field('name'), None,
                    {'name': value, 'name__negate': str(negate).lower()}, None, None, 'name')

    result = f.queryset(None, Artist.objects.all())
    value = list(result.values_list('name', flat=True))
    assert value == expected


def test_factory(fixtures):
    F = ValueFilter.factory(title='CustomTitle')
    f = F(Artist._meta.get_field('name'), None,
          {'name': 'a1', 'name__negate': 'false'}, None, None, 'name')

    result = f.queryset(None, Artist.objects.all())
    value = list(result.values_list('name', flat=True))
    assert value == ['a1']


def test_factory_compat(fixtures):
    field_name, F = ValueFilter.factory('name', title='CustomTitle')
    f = F(Artist._meta.get_field(field_name), None,
          {'name': 'a1', 'name__negate': 'false'}, None, None, 'name')

    result = f.queryset(None, Artist.objects.all())
    value = list(result.values_list('name', flat=True))
    assert value == ['a1']


@pytest.mark.parametrize('value,negate,expected', [('n', False, []),
                                                   ('a1', False, ['a1']),
                                                   ('a1', True, ['a2', 'b1', 'c1']),
                                                   ])
def test_MultiValueTextFieldFilter(fixtures, value, negate, expected):
    f = MultiValueFilter(Artist._meta.get_field('name'), None,
                         {'name__in': value, 'name__in__negate': str(negate).lower()}, None, None, 'name')
    result = f.queryset(None, Artist.objects.all())
    value = list(result.values_list('name', flat=True))
    assert value == expected