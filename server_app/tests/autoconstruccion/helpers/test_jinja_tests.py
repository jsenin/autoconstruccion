import pytest
from autoconstruccion.helpers.helpers import startswith


@pytest.mark.parametrize("string", ['Hola', 'Horacio'])
def test_startwith_test_detect_prefix(string):
    prefix = 'Ho'
    assert startswith(string, prefix)


@pytest.mark.parametrize("string", ['Fulano', 'patricio'])
def test_startwith_test_detect_prefix(string):
    prefix = 'Ho'
    assert not startswith(string, prefix)

