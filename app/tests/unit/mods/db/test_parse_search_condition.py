import pytest

from app.mods.db.parse_search_condition import parse_search_condition
from app.models.User import User
from app.models.Article import Article


@pytest.mark.parametrize(
    ['conditions', 'is_and_condtion', 'filters'],
    [
        pytest.param(
            ['username:=user1', 'or', 'create_at:=2025/03/30'],
            False,
            [User.username == 'user1', User.create_at == '2025/03/30']
            ),
        pytest.param(
            ['username:=user1', 'create_at:=2025/03/30'],
            True,
            [User.username == 'user1', User.create_at == '2025/03/30']
        )
    ]
)
def test_parse_search_condition_and_or_condtion(conditions, is_and_condtion, filters):
    """
    parse_search_conditionのand/or分岐確認テスト用関数
    Args:
        condtions: list
            実際にユーザーから入力された検索条件のリスト
        is_and_conditon: bool
            戻り値となる検索方法のbool値
            True: and検索
            False: or検索
        filters: list
            戻り値となる検索条件のリスト
    """
    ret_is_and_conditions, ret_filters = parse_search_condition(conditions)
    assert is_and_condtion == ret_is_and_conditions
    assert str(filters[0]) == str(ret_filters[0])
    assert str(filters[1]) == str(ret_filters[1])
    
    
@pytest.mark.parametrize(
    ['search_str', 'filters'],
    [
        pytest.param(
            ['python'],
            [Article.title.like('%python%'),Article.body.like('%python%')],
        )
    ]
)
def test_parse_search_condition_only_str(
    search_str,
    filters
):
    ret_is_and_conditions, ret_filters = parse_search_condition(search_str)
    assert str(filters[0]) == str(ret_filters[0])
    assert str(filters[1]) == str(ret_filters[1])


@pytest.mark.parametrize(
    ['search_strs', 'filters'],
    [
        pytest.param(
            ['username:=user1'],
            [User.username == 'user1']
        ),
        pytest.param(
            ['create_at:>=2025/03/03'],
            [User.create_at >= '2025/03/03']
        ),
        pytest.param(
            ['create_at:<=2025/03/03'],
            [User.create_at <= '2025/03/03']
        ),
        pytest.param(
            ['create_at:>2025/03/03'],
            [User.create_at > '2025/03/03']
        ),
        pytest.param(
            ['create_at:<2025/03/03'],
            [User.create_at < '2025/03/03']
        ),
        pytest.param(
            ['create_at:[2025/03/03,2025/03/04]'],
            [User.create_at.between('2025/03/03', '2025/03/04')]
        ),
        pytest.param(
            ['adsdf:=user1'],
            [Article.title.like('%user1%'), Article.body.like('%user1%')]
        )
    ]
)
def test_parse_search_condition_match(search_strs, filters):
    """
    マッチすべき条件にマッチすることを確認する。
    """
    ret_is_and_condtion, ret_filters = parse_search_condition(search_strs)
    assert str(filters[0]) == str(ret_filters[0])