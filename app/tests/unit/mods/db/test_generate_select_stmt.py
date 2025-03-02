import pytest
from sqlmodel import select, or_
from datetime import datetime

from app.models.User import User
from app.mods.db.generate_select_stmt import generate_select_stmt


@pytest.mark.parametrize(
    ['currect_stmt_str', 'args'],
    [
        pytest.param(
            select(User).where(User.username == 'test_user').compile(compile_kwargs={"literal_binds": True}),
            [User.username == 'test_user']
            ),
        pytest.param(
            select(User).where(User.username.like('%test_user%')).compile(compile_kwargs={"literal_binds": True}),
            [User.username.like(f'%test_user%')]
            ),
        pytest.param(
            select(User).where(User.username.startswith('test_user')).compile(compile_kwargs={"literal_binds": True}),
            [User.username.startswith('test_user')]
            ),
        pytest.param(
            select(User).where(User.create_at < datetime(2024, 1, 1)).compile(compile_kwargs={"literal_binds": True}),
            [User.create_at < datetime(2024, 1, 1)]
            ),
        pytest.param(
            select(User).where(User.create_at.between(datetime(2024, 1, 1), datetime(2025, 1, 1))).compile(compile_kwargs={"literal_binds": True}),
            [User.create_at.between(datetime(2024, 1, 1), datetime(2025, 1, 1))]
            ),
    ]
)
def test_generate_select_unit_stmt(currect_stmt_str, args):
    """generate_select_stmtのテスト"""
    generated_stmt_str = str(generate_select_stmt(model=User, requirements=args).compile(compile_kwargs={"literal_binds": True}))
    assert str(currect_stmt_str) == generated_stmt_str


@pytest.mark.parametrize(
    ['currect_stmt_str', 'args'],
    [
        pytest.param(
           select(User).where(User.username == 'test_user').where(User.create_at < datetime(2024,1,1)).compile(compile_kwargs={"literal_binds": True}),
            [User.username == 'test_user', User.create_at < datetime(2024,1,1)]
            ),
        pytest.param(
            select(User).where(User.username.like('%test_user%')).where(User.create_at < datetime(2024,1,1)).compile(compile_kwargs={"literal_binds": True}),
            [User.username.like(f'%test_user%'), User.create_at < datetime(2024,1,1)]
            ),
        pytest.param(
            select(User).where(User.username.startswith('test_user')).where(User.create_at < datetime(2024,1,1)).compile(compile_kwargs={"literal_binds": True}),
            [User.username.startswith('test_user'), User.create_at < datetime(2024,1,1)]
            ),
        pytest.param(
            select(User).where(User.create_at < datetime(2024, 1, 1)).where(User.is_admin == True).compile(compile_kwargs={"literal_binds": True}),
            [User.create_at < datetime(2024, 1, 1), User.is_admin == True]
            ),
        pytest.param(
            select(User).where(User.create_at.between(datetime(2024, 1, 1), datetime(2025, 1, 1))).where(User.is_admin == True).compile(compile_kwargs={"literal_binds": True}),
            [User.create_at.between(datetime(2024, 1, 1), datetime(2025, 1, 1)), User.is_admin == True]
            ),
    ]
)
def test_generate_select_multi_stmt(currect_stmt_str, args):
    """generate_select_stmtのテスト"""
    generated_stmt_str = str(generate_select_stmt(model=User, requirements=args).compile(compile_kwargs={"literal_binds": True}))
    assert str(currect_stmt_str) == generated_stmt_str


@pytest.mark.parametrize(
    ['currect_stmt_str', 'args', 'range'],
    [
        pytest.param(
            select(User).where(User.username == 'test_user').where(User.create_at < datetime(2024,1,1)).offset(1).compile(compile_kwargs={"literal_binds": True}),
            [User.username == 'test_user', User.create_at < datetime(2024,1,1)],
            [1,None]
            ),
        pytest.param(
            select(User).where(User.username.like('%test_user%')).where(User.create_at < datetime(2024,1,1)).limit(1).compile(compile_kwargs={"literal_binds": True}),
            [User.username.like(f'%test_user%'), User.create_at < datetime(2024,1,1)],
            [None, 1]
            ),
        pytest.param(
            select(User).where(User.username.startswith('test_user')).where(User.create_at < datetime(2024,1,1)).offset(1).limit(2).compile(compile_kwargs={"literal_binds": True}),
            [User.username.startswith('test_user'), User.create_at < datetime(2024,1,1)],
            [1,2]
            ),
    ]
)
def test_generate_select_offset_stmt(currect_stmt_str, args, range):
    """generate_select_stmtのテスト"""
    generated_stmt_str = str(generate_select_stmt(model=User, requirements=args, offset=range[0], limit=range[1]).compile(compile_kwargs={"literal_binds": True}))
    assert str(currect_stmt_str) == generated_stmt_str


@pytest.mark.parametrize(
    ['currect_stmt_str', 'requirements', 'is_and_condition'],
    [
        pytest.param(
            select(User).where(User.create_at < datetime(2024, 1, 1)).where(User.is_admin == True).compile(compile_kwargs={"literal_binds": True}),
            [User.create_at < datetime(2024, 1, 1), User.is_admin == True],
            True
            ),
        pytest.param(
            select(User).where(or_(User.create_at.between(datetime(2024, 1, 1), datetime(2025, 1, 1)), User.is_admin == True)).compile(compile_kwargs={"literal_binds": True}),
            [User.create_at.between(datetime(2024, 1, 1), datetime(2025, 1, 1)), User.is_admin == True],
            False
            ),
    ]
)
def test_generate_select_condition_stmt(currect_stmt_str, requirements, is_and_condition):
    """generate_select_stmtのテスト"""
    generated_stmt_str = str(generate_select_stmt(model=User, requirements=requirements, is_and_condition=is_and_condition).compile(compile_kwargs={"literal_binds": True}))
    assert str(currect_stmt_str) == generated_stmt_str