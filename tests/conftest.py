import pytest

@pytest.fixture
def assert_list_match():
    '''2つのリストが同じ要素を格納しているかチェックする関数'''

    def _assert_list_match(list1, list2):
        assert sorted(list1) == sorted(list2)

    return _assert_list_match